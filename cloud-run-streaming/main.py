import os
import json
import asyncio
import time
import tempfile
import logging
from typing import AsyncGenerator, List, Dict, Any
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import openai
from google.cloud import firestore, secretmanager, storage
from docx import Document
from collections import defaultdict
from dotenv import load_dotenv

# Load environment variables from .env file for local development
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Chat-PRD Streaming API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Google Cloud services
try:
    db = firestore.Client()
    secret_client = secretmanager.SecretManagerServiceClient()
    storage_client = storage.Client()
    logger.info("Google Cloud services initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Google Cloud services: {e}")
    db = None
    secret_client = None
    storage_client = None

# Initialize OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Rate limiting
class RateLimiter:
    def __init__(self, max_requests: int = 20, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
    
    def is_allowed(self, client_ip: str) -> bool:
        now = time.time()
        client_requests = self.requests[client_ip]
        
        # Remove old requests
        client_requests[:] = [req_time for req_time in client_requests 
                             if now - req_time < self.window_seconds]
        
        if len(client_requests) >= self.max_requests:
            return False
        
        client_requests.append(now)
        return True

rate_limiter = RateLimiter()

# Pydantic models
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    conversation: List[ChatMessage]
    user_id: str = None

class ChatResponse(BaseModel):
    response: str
    tokenUsage: Dict[str, int] = None

class ExportRequest(BaseModel):
    conversation: List[ChatMessage]

# Utility functions
async def get_openai_key():
    """Retrieve OpenAI API key from Secret Manager or environment"""
    try:
        # First try environment variable (for local development)
        api_key = os.environ.get('OPENAI_API_KEY')
        if api_key:
            logger.info("Using OpenAI API key from environment variable")
            return api_key
        
        # Try Secret Manager
        if secret_client:
            project_id = os.environ.get('GOOGLE_CLOUD_PROJECT', 'explo-website-tools')
            name = f"projects/{project_id}/secrets/openai-api-key/versions/latest"
            response = secret_client.access_secret_version(request={"name": name})
            api_key = response.payload.data.decode("UTF-8")
            logger.info("Using OpenAI API key from Secret Manager")
            return api_key
        
        raise Exception("No OpenAI API key found in environment or Secret Manager")
    except Exception as e:
        logger.error(f"Failed to get OpenAI API key: {e}")
        raise HTTPException(status_code=500, detail=f"API key configuration error: {str(e)}")

def estimate_tokens(text: str) -> int:
    """Rough token estimation"""
    return max(1, len(text) // 4)

# Rate limiting middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "unknown"
    
    if request.url.path.startswith("/chat"):
        if not rate_limiter.is_allowed(client_ip):
            raise HTTPException(
                status_code=429, 
                detail="Rate limit exceeded. Please slow down."
            )
    
    response = await call_next(request)
    return response

# This is the original, simple way to create the client.
async def create_openai_client():
    """Creates an OpenAI client."""
    api_key = await get_openai_key()
    return openai.AsyncOpenAI(api_key=api_key)

# Streaming function
async def stream_openai_response(messages: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
    """Stream OpenAI response chunks with comprehensive logging"""
    request_id = f"req_{int(time.time())}"
    logger.info(f"Starting stream {request_id}")
    
    try:
        client = await create_openai_client()
        
        start_time = time.time()
        chunk_count = 0
        
        # Create streaming completion
        stream = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=True,
            max_tokens=2048,
            temperature=0.7
        )
        
        full_response = ""
        
        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_response += content
                chunk_count += 1
                
                # Yield individual chunk
                yield f"data: {json.dumps({
                    'type': 'chunk', 
                    'content': content,
                    'chunk_id': chunk_count,
                    'request_id': request_id
                })}\n\n"
        
        duration = time.time() - start_time
        logger.info(f"Stream {request_id} completed in {duration:.2f}s with {chunk_count} chunks")
        
        # Final message with complete response
        yield f"data: {json.dumps({
            'type': 'complete', 
            'content': full_response,
            'metadata': {
                'duration': duration,
                'chunk_count': chunk_count,
                'request_id': request_id
            }
        })}\n\n"
        
        yield "data: [DONE]\n\n"
        
        # Close client properly
        await client.close()
        
    except Exception as e:
        logger.error(f"Stream {request_id} failed: {str(e)}")
        yield f"data: {json.dumps({
            'type': 'error', 
            'content': f"Streaming error: {str(e)}", 
            'request_id': request_id
        })}\n\n"

# API endpoints
@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Streaming chat endpoint using Server-Sent Events"""
    try:
        # Prepare messages for OpenAI (last 20 messages for context)
        messages = []
        for msg in request.conversation[-20:]:
            if msg.role in ['system', 'user', 'assistant']:
                messages.append({
                    'role': msg.role,
                    'content': msg.content
                })
        
        if not messages:
            raise HTTPException(status_code=400, detail="No valid messages in conversation")
        
        return StreamingResponse(
            stream_openai_response(messages),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",  # Disable Nginx buffering
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
            }
        )
    except Exception as e:
        logger.error(f"Streaming endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat_fallback(request: ChatRequest):
    """Fallback non-streaming endpoint for compatibility"""
    try:
        client = await create_openai_client()
        
        # Prepare messages
        messages = []
        for msg in request.conversation[-20:]:
            if msg.role in ['system', 'user', 'assistant']:
                messages.append({
                    'role': msg.role,
                    'content': msg.content
                })
        
        if not messages:
            raise HTTPException(status_code=400, detail="No valid messages in conversation")
        
        # Create completion
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=2048,
            temperature=0.7
        )
        
        result = ChatResponse(
            response=response.choices[0].message.content,
            tokenUsage={
                "promptTokens": response.usage.prompt_tokens,
                "completionTokens": response.usage.completion_tokens,
                "totalTokens": response.usage.total_tokens
            }
        )
        
        # Close client properly
        await client.close()
        return result
    except Exception as e:
        logger.error(f"Chat fallback error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/export")
async def export_prd(request: ExportRequest):
    """Export PRD functionality (simplified version of existing)"""
    try:
        if len(request.conversation) <= 1:
            raise HTTPException(status_code=400, detail="No conversation to export")
        
        api_key = await get_openai_key()
        client = openai.AsyncOpenAI(api_key=api_key)
        
        # Create PRD generation prompt
        conversation_text = "\n".join([
            f"{msg.role.upper()}: {msg.content}" 
            for msg in request.conversation 
            if msg.role != 'system'
        ])
        
        prd_prompt = f"""Based on the following conversation, generate a comprehensive Product Requirements Document (PRD). 
Structure it with clear sections including:

1. **Product Overview**: Brief description and goals
2. **User Stories**: Key user personas and their needs  
3. **Features & Functionality**: Detailed feature descriptions
4. **Technical Requirements**: High-level technical considerations
5. **Success Metrics**: How success will be measured

Format using markdown with proper headers and bullet points.

CONVERSATION:
{conversation_text}

PRD:"""

        # Generate PRD content
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prd_prompt}],
            max_tokens=4096,
            temperature=0.5
        )
        
        prd_content = response.choices[0].message.content
        
        # Create Word document
        doc = Document()
        doc.add_heading('Product Requirements Document', 0)
        doc.add_paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        doc.add_page_break()
        
        # Simple markdown to Word conversion
        lines = prd_content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                doc.add_heading(line[2:], level=1)
            elif line.startswith('## '):
                doc.add_heading(line[3:], level=2)
            elif line.startswith('### '):
                doc.add_heading(line[4:], level=3)
            elif line.startswith('- ') or line.startswith('* '):
                doc.add_paragraph(line[2:], style='List Bullet')
            elif line:
                doc.add_paragraph(line)
        
        # Save to temporary file
        temp_filename = f"PRD_{int(time.time())}.docx"
        temp_path = os.path.join(tempfile.gettempdir(), temp_filename)
        doc.save(temp_path)
        
        # Upload to Google Cloud Storage (if available)
        if storage_client:
            try:
                project_id = os.environ.get('GOOGLE_CLOUD_PROJECT', 'explo-website-tools')
                bucket_name = f'{project_id}.firebasestorage.app'
                bucket = storage_client.bucket(bucket_name)
                blob_path = f'exports/{temp_filename}'
                blob = bucket.blob(blob_path)
                
                blob.upload_from_filename(temp_path)
                
                # Generate signed URL
                download_url = blob.generate_signed_url(
                    expiration=3600,  # 1 hour
                    method='GET'
                )
                
                # Clean up temp file
                os.remove(temp_path)
                
                return {"downloadURL": download_url, "fileName": temp_filename}
            except Exception as storage_error:
                logger.error(f"Storage upload failed: {storage_error}")
                # Fallback: return local file (for development)
                return {"error": "Storage upload failed", "localFile": temp_path}
        else:
            return {"error": "Storage not configured", "localFile": temp_path}
            
    except Exception as e:
        logger.error(f"Export error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Chat-PRD Streaming API", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port) 