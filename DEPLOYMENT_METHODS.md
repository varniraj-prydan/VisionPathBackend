# Cloud Run Deployment Methods

There are 3 main ways to deploy to Google Cloud Run. Choose the method that best fits your workflow:

## 🔧 Method 1: Container Method
**Best for**: When you want full control over the Docker build process

### Prerequisites:
- Docker installed locally
- Google Cloud SDK installed

### Deploy:
```bash
# Windows
deploy-container.bat

# Manual commands
docker build -t gcr.io/PROJECT_ID/voice-learning-tutor .
docker push gcr.io/PROJECT_ID/voice-learning-tutor
gcloud run deploy voice-learning-tutor --image=gcr.io/PROJECT_ID/voice-learning-tutor --region=us-central1
```

### Pros:
- Full control over Docker build
- Can test container locally first
- Faster subsequent deployments (cached layers)

### Cons:
- Requires Docker installed locally
- Manual image management

---

## 📦 Method 2: Source Method
**Best for**: Quick deployments without managing Docker

### Prerequisites:
- Google Cloud SDK installed

### Deploy:
```bash
# Windows
deploy-source.bat

# Manual command
gcloud run deploy voice-learning-tutor --source=. --region=us-central1
```

### Pros:
- No Docker required locally
- Simplest deployment method
- Automatic buildpack detection

### Cons:
- Less control over build process
- Slower builds (no local caching)

---

## ☁️ Method 3: Cloud Build Method
**Best for**: CI/CD pipelines and automated deployments

### Prerequisites:
- Google Cloud SDK installed
- cloudbuild.yaml configuration file

### Deploy:
```bash
# Windows
deploy.bat

# Manual command
gcloud builds submit --config cloudbuild.yaml .
```

### Pros:
- Perfect for CI/CD
- Reproducible builds
- Can include additional build steps
- Build history in Cloud Console

### Cons:
- Requires cloudbuild.yaml configuration
- Slightly more complex setup

---

## 🚀 Quick Comparison

| Method | Speed | Control | Complexity | Best For |
|--------|-------|---------|------------|----------|
| Container | Fast* | High | Medium | Local development |
| Source | Medium | Low | Low | Quick deployments |
| Cloud Build | Medium | High | High | Production/CI-CD |

*After initial build

## 📋 Common Configuration

All methods use the same Cloud Run configuration:
- **Memory**: 2GB
- **CPU**: 2 cores  
- **Timeout**: 5 minutes
- **Region**: us-central1
- **Max Instances**: 10
- **Port**: 8080

## 🔍 Which Method Should You Use?

### For Development:
- **Container Method** - Build and test locally, then deploy

### For Quick Testing:
- **Source Method** - Fastest to get started

### For Production:
- **Cloud Build Method** - Best for automated deployments

## 🛠️ Post-Deployment Commands

```bash
# Get service URL
gcloud run services describe voice-learning-tutor --region=us-central1 --format="value(status.url)"

# View logs
gcloud logs tail --service=voice-learning-tutor

# Update service (any method)
# Just run the deployment script again
```

## 🔧 Troubleshooting

### Docker Issues (Container Method):
```bash
# Configure Docker for GCR
gcloud auth configure-docker

# Test local build
docker build -t test-image .
docker run -p 8080:8080 test-image
```

### Build Issues (Source Method):
- Ensure `requirements.txt` is present
- Check Python version compatibility
- Verify all dependencies are listed

### Cloud Build Issues:
- Check `cloudbuild.yaml` syntax
- Verify Cloud Build API is enabled
- Check build logs in Cloud Console