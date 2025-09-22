# Deploy to Cloud Run via Web UI (No CLI Required)

## 🌐 Method: Google Cloud Console Web Interface

**Perfect for**: No CLI tools installed, browser-based deployment

### Step 1: Prepare Your Code
1. Zip your entire project folder
2. Make sure these files are included:
   - `main.py`
   - `requirements.txt` 
   - `Dockerfile`
   - `services/` folder
   - All other project files

### Step 2: Go to Google Cloud Console
1. Open [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable billing for your project

### Step 3: Enable Required APIs
Go to **APIs & Services** → **Library** and enable:
- Cloud Run API
- Cloud Build API
- Container Registry API
- Vertex AI API
- Cloud Speech-to-Text API
- Cloud Text-to-Speech API
- Cloud Firestore API

### Step 4: Deploy via Cloud Run Console

#### Option A: Deploy from Source (Recommended)
1. Go to **Cloud Run** in the console
2. Click **Create Service**
3. Select **Deploy one revision from a source repository**
4. Click **Set up with Cloud Build**
5. Choose **Repository provider**: GitHub/Bitbucket/etc. OR upload zip
6. Configure:
   - **Service name**: `voice-learning-tutor`
   - **Region**: `us-central1`
   - **CPU allocation**: `CPU is always allocated`
   - **Memory**: `2 GiB`
   - **Maximum number of instances**: `10`
   - **Port**: `8080`
7. Under **Environment Variables**, add:
   - `GOOGLE_CLOUD_PROJECT` = `your-project-id`
8. Click **Create**

#### Option B: Deploy from Container Registry
1. First upload your code to Cloud Shell:
   - Go to **Cloud Shell** (terminal icon in top bar)
   - Upload your zip file
   - Extract: `unzip your-project.zip`
   - Build: `docker build -t gcr.io/PROJECT_ID/voice-learning-tutor .`
   - Push: `docker push gcr.io/PROJECT_ID/voice-learning-tutor`
2. Then deploy via Cloud Run console using the container image

### Step 5: Alternative - Cloud Shell (Browser Terminal)
If you want to use CLI but don't want to install locally:

1. Open **Cloud Shell** in Google Cloud Console
2. Upload your project zip file
3. Extract and navigate to folder:
   ```bash
   unzip VisionPathBackend.zip
   cd VisionPathBackend
   ```
4. Run deployment:
   ```bash
   gcloud run deploy voice-learning-tutor \
     --source=. \
     --region=us-central1 \
     --allow-unauthenticated \
     --memory=2Gi \
     --cpu=2 \
     --port=8080
   ```

### Step 6: Test Your Deployment
1. Get the service URL from Cloud Run console
2. Test endpoints:
   - `GET /health` - Health check
   - `POST /capture` - Upload audio file

## 🎯 Easiest Method Summary:

1. **Zip your project**
2. **Go to Cloud Console → Cloud Run**
3. **Click "Create Service"**
4. **Select "Deploy from source"**
5. **Upload your zip or connect repository**
6. **Configure settings and deploy**

## 📱 Mobile/Tablet Deployment:
You can even deploy from mobile using the Google Cloud Console mobile app or mobile browser!

## 🔧 No-Code Required:
- No CLI installation needed
- No Docker knowledge required
- Everything done through web interface
- Google handles the containerization automatically