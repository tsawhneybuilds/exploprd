# PRD AI Chatbot - Explo

A comprehensive AI-powered Product Requirements Document (PRD) assistant that helps users create detailed PRDs through an interactive chat interface. The application features real-time streaming responses, document export capabilities, and is built with a modern serverless architecture.

## 🏗️ Project Architecture

### Overview
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│                 │    │                  │    │                     │
│  Frontend (Web) │───▶│ Firebase Hosting │───▶│ Cloud Run / Functions│
│   index.html    │    │   (Routing)      │    │   (API Endpoints)   │
│                 │    │                  │    │                     │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
                                 │                        │
                                 ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────────┐
                       │                  │    │                     │
                       │  Static Assets   │    │   OpenAI API        │
                       │  (HTML, CSS, JS) │    │   Firestore DB      │
                       │                  │    │   Secret Manager    │
                       └──────────────────┘    │   Cloud Storage     │
                                               └─────────────────────┘
```

### Technology Stack
- **Frontend**: Vanilla JavaScript, HTML5, CSS3, Tailwind CSS
- **Backend**: FastAPI (Python 3.11) on Google Cloud Run + Firebase Functions
- **Database**: Google Firestore
- **Storage**: Google Cloud Storage
- **Hosting**: Firebase Hosting
- **AI**: OpenAI GPT-4o-mini
- **Authentication**: Google Secret Manager
- **CI/CD**: Google Cloud Build

## 📁 Project Structure

```
chatprd/
├── public/
│   ├── index.html                 # Main web application
│   ├── logo-explo.png            # Explo logo
│   └── test-analytics.html       # Analytics testing page
├── cloud-run-streaming/          # Primary Cloud Run service
│   ├── main.py                   # FastAPI application
│   ├── requirements.txt          # Python dependencies
│   ├── Dockerfile               # Container configuration
│   ├── cloudbuild.yaml          # Cloud Build configuration
│   ├── run-local.sh             # Local development script
│   ├── test-local.py            # Local testing utilities
│   ├── test-streaming.py        # Streaming functionality tests
│   └── debug_client.py          # Debug utilities
├── functions/                    # Firebase Functions (legacy/fallback)
│   ├── main.py                  # Legacy Firebase Functions
│   └── requirements.txt         # Function dependencies
├── firebase.json                # Firebase configuration & routing
├── firestore.rules             # Database security rules
├── firestore.indexes.json      # Database indexes
├── storage.rules               # Storage security rules
├── deploy-streaming.sh         # Deployment automation script
└── package.json               # Node.js configuration
```

## 🚀 Functions & Endpoints

### Cloud Run Service (Primary)
**Location**: `cloud-run-streaming/main.py`  
**Deployed to**: Google Cloud Run (`chat-prd-streaming`)  
**URL**: `https://chat-prd-streaming-142797649545.us-central1.run.app`

| Endpoint | Method | Purpose | Features |
|----------|--------|---------|----------|
| `/` | GET | Service info | Returns service metadata |
| `/health` | GET | Health check | Monitoring endpoint |
| `/warmup` | GET | **Cold start elimination** | Initializes services for faster responses |
| `/chat/stream` | POST | **Streaming chat** | Real-time streaming AI responses |
| `/chat` | POST | Non-streaming chat | Fallback for older browsers |
| `/export` | POST | **PRD document export** | Generates downloadable Word documents |
| `/optimize` | POST | **Conversation optimization** | Reduces token usage for long conversations |

### Firebase Functions (Legacy/Fallback)
**Location**: `functions/main.py`  
**Deployed to**: Firebase Functions  

| Function | Purpose | Status |
|----------|---------|--------|
| `chat_simple` | Basic chat functionality | Legacy fallback |
| `export_simple` | Document export | Legacy fallback |
| `optimize_conversation` | **Active** - Token optimization | Currently used via Firebase routing |

## 🔧 Deployment Configuration

### Firebase Hosting Routes (`firebase.json`)
```json
{
  "/chat/**": "Cloud Run - chat-prd-streaming",
  "/export": "Cloud Run - chat-prd-streaming", 
  "/health": "Cloud Run - chat-prd-streaming",
  "/optimize": "Firebase Functions - optimize_conversation",
  "/**": "Static hosting - index.html"
}
```

### Google Cloud Projects
- **Primary Project**: `explo-website-tools`
- **Firebase Site**: `explochatprd`
- **Service Account**: `142797649545-compute@developer.gserviceaccount.com`

## 🛠️ Setup & Deployment

### Prerequisites
```bash
# Required tools
gcloud CLI (authenticated as tanush@explo.co)
firebase CLI
Node.js & npm
Python 3.11+
Docker (for local development)

# Required access
Google Cloud Project: explo-website-tools
OpenAI API account with billing enabled
Firebase project access
```

### Environment Variables & Secrets
```bash
# Google Secret Manager (Production)
OPENAI_API_KEY     # Stored in Secret Manager
GOOGLE_CLOUD_PROJECT=explo-website-tools

# Local Development (.env file)
OPENAI_API_KEY=your-api-key-here
GOOGLE_CLOUD_PROJECT=explo-website-tools
PORT=8080
```

### Quick Deployment
```bash
# 1. Deploy Cloud Run service
./deploy-streaming.sh explo-website-tools

# 2. Deploy Firebase hosting
firebase deploy --only hosting

# 3. Deploy Firebase functions (if needed)
firebase deploy --only functions
```

### Manual Deployment Steps

#### Cloud Run Service
```bash
cd cloud-run-streaming

# Build container
gcloud builds submit --tag gcr.io/explo-website-tools/chat-prd-streaming

# Deploy service
gcloud run deploy chat-prd-streaming \
  --image gcr.io/explo-website-tools/chat-prd-streaming \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --timeout 300s \
  --concurrency 80 \
  --min-instances 0 \
  --max-instances 10
```

#### Firebase Services
```bash
# Deploy hosting & functions
firebase deploy

# Deploy specific services
firebase deploy --only hosting
firebase deploy --only functions
firebase deploy --only firestore:rules
```

## 🔄 Key Features Explained

### 1. Cold Start Elimination
**Problem**: Cloud Run containers sleep when unused, causing 10-15 second delays  
**Solution**: Warmup endpoint called automatically on page load
- Page loads → `/warmup` called immediately  
- Service initializes in ~150ms
- First chat response: ~2 seconds (vs 15+ seconds cold)
- **Cost**: $0/month (only warms up when needed)

### 2. Real-time Streaming
**Technology**: Server-Sent Events (SSE) with FastAPI
- Text appears token-by-token as AI generates it
- Fallback to non-streaming for older browsers
- Progressive enhancement approach

### 3. Token Optimization
**Problem**: Long conversations hit token limits and cost more
**Solution**: Automatic conversation summarization
- Triggers at 3000+ tokens
- Preserves context while reducing size
- Happens silently in background

### 4. Document Export
**Process**: Conversation → AI Analysis → Word Document
- Extracts key PRD components from chat history
- Generates structured Word document (.docx)
- Downloads automatically via Cloud Storage

## 📊 Performance & Scaling

### Current Capacity
- **Max instances**: 10
- **Concurrency per instance**: 80 requests
- **Total concurrent capacity**: 800 requests
- **Realistic user capacity**: 2,000-5,000 users
- **Response time**: 1-3 seconds (after warmup)

### Cost Optimization
- **Min instances**: 0 (scales to zero when not used)
- **Warmup strategy**: On-demand via page load
- **Token optimization**: Automatic conversation compression
- **Estimated cost**: Pay-per-use (very low for typical traffic)

## 🧪 Testing & Development

### Local Development
```bash
cd cloud-run-streaming

# Set up environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your-key-here" > .env

# Run locally
./run-local.sh
# or
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### Testing Scripts
```bash
# Test local service
python test-local.py http://localhost:8080

# Test streaming functionality
python test-streaming.py

# Test production service
python test-local.py https://chat-prd-streaming-142797649545.us-central1.run.app

# Quick health check
curl https://chat-prd-streaming-142797649545.us-central1.run.app/health
```

## 🔍 Monitoring & Maintenance

### Health Checks
```bash
# Service health
curl https://chat-prd-streaming-142797649545.us-central1.run.app/health

# Warmup performance
curl -w "\nTotal time: %{time_total}s\n" \
  https://chat-prd-streaming-142797649545.us-central1.run.app/warmup
```

### Log Monitoring
```bash
# Cloud Run logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=chat-prd-streaming" --limit=50

# Firebase Functions logs
firebase functions:log
```

### Key Metrics to Monitor
- **Response time**: First token < 2 seconds
- **Success rate**: > 95% successful requests  
- **Error rate**: < 5% failed requests
- **Warmup performance**: < 200ms warmup time
- **Token usage**: Monitor for cost optimization

## 🚨 Troubleshooting

### Common Issues

**1. Slow first responses**
- Check warmup endpoint: `/warmup`
- Verify min-instances is set correctly
- Monitor cold start logs

**2. OpenAI API errors**
- Verify API key in Secret Manager
- Check OpenAI account billing/quotas
- Review rate limiting settings

**3. Deployment failures**
- Ensure correct Google Cloud project
- Check service account permissions
- Verify API enablement

**4. Streaming not working**
- Check browser compatibility
- Verify CORS configuration
- Test fallback endpoints

### Debug Commands
```bash
# Check service status
gcloud run services describe chat-prd-streaming --region us-central1

# View recent logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=chat-prd-streaming" --limit=20

# Test specific endpoints
curl -X POST https://chat-prd-streaming-142797649545.us-central1.run.app/chat \
  -H "Content-Type: application/json" \
  -d '{"conversation":[{"role":"user","content":"test"}]}'
```

## 🔐 Security Considerations

### API Keys & Secrets
- **OpenAI API key**: Stored in Google Secret Manager
- **Service account**: Least privilege access
- **CORS**: Configured for production domains
- **Rate limiting**: Built-in protection (20 requests/min per IP)

### Database Security
- **Firestore rules**: Restrict access to authenticated operations
- **Storage rules**: Control file upload/download permissions
- **Function security**: Input validation and sanitization

## 🔄 Backup & Recovery

### Data Backup
- **Firestore**: Automatic daily backups via Google Cloud
- **Secrets**: Backed up in Secret Manager versions
- **Code**: Version controlled in GitHub (`tsawhneybuilds/exploprd`)

### Rollback Process
```bash
# Rollback Cloud Run service
gcloud run services update chat-prd-streaming --region us-central1 --revision [PREVIOUS_REVISION]

# Rollback Firebase hosting
firebase hosting:clone SOURCE_SITE_ID:SOURCE_VERSION_ID TARGET_SITE_ID

# Rollback to previous Firebase config
cp firebase.json.backup firebase.json
firebase deploy --only hosting
```

## 🤝 Handover Checklist

For anyone taking over this project:

### Immediate Access Needed
- [ ] Google Cloud Console access to `explo-website-tools`
- [ ] Firebase Console access to `explochatprd` project  
- [ ] GitHub repository access: `tsawhneybuilds/exploprd`
- [ ] OpenAI API account access (or new API key)

### Knowledge Transfer
- [ ] Review this README thoroughly
- [ ] Run local development setup
- [ ] Test deployment process
- [ ] Understand the warmup strategy
- [ ] Review monitoring and alerting setup

### Critical Files to Understand
- [ ] `cloud-run-streaming/main.py` - Main service logic
- [ ] `public/index.html` - Frontend application  
- [ ] `firebase.json` - Routing and configuration
- [ ] `deploy-streaming.sh` - Deployment automation

### Maintenance Schedule
- **Weekly**: Monitor logs and performance metrics
- **Monthly**: Review OpenAI API usage and costs
- **Quarterly**: Update dependencies and security patches
- **As needed**: Scale instance limits based on traffic

## 📞 Support & Documentation

### Additional Resources
- [STREAMING_README.md](./STREAMING_README.md) - Detailed streaming implementation
- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Firebase Hosting Documentation](https://firebase.google.com/docs/hosting)
- [OpenAI API Documentation](https://platform.openai.com/docs)

### Contact Information
- **Original Developer**: Tanush Sawhney
- **GitHub**: `tsawhneybuilds/exploprd`
- **Project**: Explo PRD AI Assistant

---

**Last Updated**: January 2025  
**Version**: 2.0 (Streaming Implementation)  
**Status**: Production Ready ✅ 