# Voice Learning Tutor Backend

Voice-first AI learning tutor MVP using FastAPI and Google Cloud services.

## Quick Start

### 1. Clone and Setup Environment
```bash
git clone <repository-url>
cd VisionPathBackend
python -m venv venv
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

### 2. Google Cloud Setup

#### Create Service Account:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Go to **IAM & Admin** → **Service Accounts**
4. Click **Create Service Account**
5. Add these roles:
   - Vertex AI User
   - Cloud Speech Client
   - Cloud Text-to-Speech Client
   - Cloud Datastore User
6. Create and download the JSON key file

#### Enable Required APIs:
```bash
gcloud services enable aiplatform.googleapis.com
gcloud services enable speech.googleapis.com
gcloud services enable texttospeech.googleapis.com
gcloud services enable firestore.googleapis.com
```

### 3. Configure Credentials
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your values:
# GOOGLE_APPLICATION_CREDENTIALS=./your-service-account.json
# GOOGLE_CLOUD_PROJECT=your-project-id
```

### 4. Run Server
```bash
python main.py
```

### 5. Test Setup
```bash
python test_services.py
```

## 🔒 Security Notes

- **Never commit** `.env` files or `*.json` credential files
- The `.gitignore` is configured to prevent accidental commits
- For production, use Google Cloud IAM roles instead of service account keys
- Rotate service account keys regularly

## 🚀 For Hackathon Judges

1. **Quick Setup**: Run `python setup_credentials.py` for guided setup
2. **Test Everything**: Use `python test_services.py` to verify all services work
3. **API Documentation**: Check `API_DOCUMENTATION.md` for endpoint details

## API Endpoints

- `POST /capture` - Upload audio file, get transcript
- `POST /create-roadmap` - Generate learning roadmap with Day 1 audio
- `GET /get-lesson/{roadmap_id}/{day}` - Fetch specific lesson
- `GET /audio/{filename}` - Serve audio files

## Testing

```bash
# Test transcript
curl -X POST "http://localhost:8000/capture" -F "audio=@test.wav"

# Test roadmap generation
curl -X POST "http://localhost:8000/create-roadmap" \
  -H "Content-Type: application/json" \
  -d '{"topic": "Python", "description": "Learn Python basics"}'
```