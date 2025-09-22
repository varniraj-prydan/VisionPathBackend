#!/bin/bash

echo "========================================"
echo " Voice Learning Tutor - Cloud Run Deploy"
echo "========================================"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "ERROR: gcloud CLI not found. Please install Google Cloud SDK."
    echo "Download from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Get current project
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)

if [ -z "$PROJECT_ID" ]; then
    echo "ERROR: No Google Cloud project set."
    echo "Run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo "Current project: $PROJECT_ID"
echo

# Enable required APIs
echo "Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable speech.googleapis.com
gcloud services enable texttospeech.googleapis.com
gcloud services enable firestore.googleapis.com

echo
echo "Starting deployment..."
echo "This will take a few minutes..."
echo

# Submit build to Cloud Build
gcloud builds submit --config cloudbuild.yaml .

if [ $? -eq 0 ]; then
    echo
    echo "========================================"
    echo " Deployment Successful!"
    echo "========================================"
    echo
    echo "Your API is now running on Cloud Run."
    echo "To get the service URL, run:"
    echo "  gcloud run services describe voice-learning-tutor --region=us-central1 --format=\"value(status.url)\""
    echo
else
    echo
    echo "========================================"
    echo " Deployment Failed!"
    echo "========================================"
    echo "Check the error messages above."
fi