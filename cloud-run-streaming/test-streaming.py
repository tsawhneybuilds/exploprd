#!/usr/bin/env python3
"""
Test script for streaming functionality
"""
import asyncio
import aiohttp
import json

async def test_streaming():
    """Test the streaming endpoint"""
    print("🧪 Testing Streaming Endpoint...")
    
    # Test data
    test_data = {
        "conversation": [
            {"role": "user", "content": "Hello! Can you tell me a short story about a cat?"}
        ]
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            # Test streaming endpoint
            async with session.post(
                'http://localhost:8080/chat/stream',
                json=test_data,
                headers={'Accept': 'text/event-stream'}
            ) as response:
                print(f"📡 Status: {response.status}")
                
                if response.status == 200:
                    print("✅ Streaming response received!")
                    print("📝 Content:")
                    
                    # Read the streaming response
                    async for line in response.content:
                        line = line.decode('utf-8').strip()
                        if line.startswith('data: '):
                            data = line[6:]  # Remove 'data: ' prefix
                            if data == '[DONE]':
                                print("🏁 Stream completed!")
                                break
                            try:
                                chunk = json.loads(data)
                                if 'choices' in chunk and chunk['choices']:
                                    content = chunk['choices'][0].get('delta', {}).get('content', '')
                                    if content:
                                        print(f"   {content}", end='', flush=True)
                            except json.JSONDecodeError:
                                continue
                else:
                    print(f"❌ Error: {response.status}")
                    text = await response.text()
                    print(f"Response: {text}")
                    
        except Exception as e:
            print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    asyncio.run(test_streaming()) 