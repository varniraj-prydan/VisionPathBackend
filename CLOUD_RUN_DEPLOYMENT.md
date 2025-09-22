# Cloud Run Deployment Guide

## Prerequisites

1. **Google Cloud SDK**: Install from [here](https://cloud.google.com/sdk/docs/install)
2. **Google Cloud Project**: Create or select a project
3. **Billing**: Enable billing on your project
4. **Authentication**: Login to gcloud

## Quick Setup

### 1. Authenticate with Google Cloud
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 2. Enable Required APIs (Automatic in deployment script)
```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable speech.googleapis.com
gcloud services enable texttospeech.googleapis.com
gcloud services enable firestore.googleapis.com
```

### 3. Deploy to Cloud Run

**Windows:**
```bash
deploy.bat
```

**Linux/Mac:**
```bash
chmod +x deploy.sh
./deploy.sh
```

**Manual Deployment:**
```bash
gcloud builds submit --config cloudbuild.yaml .
```

## Configuration Details

### Cloud Run Service Configuration
- **Service Name**: `voice-learning-tutor`
- **Region**: `us-central1`
- **Memory**: `2Gi`
- **CPU**: `2`
- **Timeout**: `300 seconds`
- **Max Instances**: `10`
- **Port**: `8080`
- **Authentication**: Public (unauthenticated)

### Environment Variables
- `GOOGLE_CLOUD_PROJECT`: Automatically set to your project ID
- `PORT`: Set to `8080` for Cloud Run

## Post-Deployment

### Get Service URL
```bash
gcloud run services describe voice-learning-tutor --region=us-central1 --format="value(status.url)"
```

### Test Your API
```bash
# Health check
curl https://YOUR_SERVICE_URL/health

# Test transcript
curl -X POST "https://YOUR_SERVICE_URL/capture" -F "audio=@test.wav"
```

### View Logs
```bash
gcloud logs tail --service=voice-learning-tutor
```

## Security Notes

- The service is deployed with `--allow-unauthenticated` for easy testing
- For production, consider adding authentication:
  ```bash
  gcloud run services update voice-learning-tutor --region=us-central1 --no-allow-unauthenticated
  ```
- Service account permissions are automatically handled by Cloud Run

## Troubleshooting

### Common Issues

1. **Build Timeout**: Increase timeout in cloudbuild.yaml
2. **Memory Issues**: Increase memory allocation in cloudbuild.yaml
3. **API Not Enabled**: Run the deployment script to enable all required APIs
4. **Permission Denied**: Ensure you have Cloud Build and Cloud Run permissions

### Debug Commands
```bash
# Check service status
gcloud run services describe voice-learning-tutor --region=us-central1

# View recent logs
gcloud logs read --service=voice-learning-tutor --limit=50

# List all Cloud Run services
gcloud run services list
```

## Cost Optimization

- Cloud Run charges only for actual usage
- Consider setting `--max-instances` based on expected load
- Use `--cpu-throttling` for cost savings if CPU isn't always needed
- Monitor usage in Google Cloud Console

## Updates

To update your service, simply run the deployment script again:
```bash
./deploy.sh  # or deploy.bat on Windows
```

The new version will be deployed with zero downtime.