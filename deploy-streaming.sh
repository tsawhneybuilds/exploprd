#!/bin/bash

# Deploy streaming Cloud Run service
# Usage: ./deploy-streaming.sh [PROJECT_ID]

set -e

# Default project ID (update this with your actual project ID)
DEFAULT_PROJECT_ID="explo-website-tools"
PROJECT_ID=${1:-$DEFAULT_PROJECT_ID}

echo "🚀 Deploying Chat-PRD Streaming Service to Cloud Run..."
echo "📦 Project ID: $PROJECT_ID"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI is not installed. Please install it first."
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Error: Please authenticate with gcloud: gcloud auth login"
    exit 1
fi

# Set the project
echo "🔧 Setting project to $PROJECT_ID..."
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build and deploy
echo "🏗️  Building and deploying to Cloud Run..."
cd cloud-run-streaming

gcloud builds submit --tag gcr.io/$PROJECT_ID/chat-prd-streaming

gcloud run deploy chat-prd-streaming \
  --image gcr.io/$PROJECT_ID/chat-prd-streaming \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 1 \
  --timeout 300s \
  --concurrency 100 \
  --min-instances 0 \
  --max-instances 10 \
  --set-env-vars GOOGLE_CLOUD_PROJECT=$PROJECT_ID

# Get the service URL
SERVICE_URL=$(gcloud run services describe chat-prd-streaming --region=us-central1 --format="value(status.url)")

echo ""
echo "✅ Deployment completed successfully!"
echo "🌐 Service URL: $SERVICE_URL"
echo "🔗 Health check: $SERVICE_URL/health"
echo ""
echo "📝 Next steps:"
echo "   1. Test the service: curl $SERVICE_URL/health"
echo "   2. Deploy Firebase hosting to use the new service: firebase deploy --only hosting"
echo "   3. Verify streaming works on your site"

cd .. 