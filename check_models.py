import vertexai
from dotenv import load_dotenv
import os

load_dotenv()

project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
print(f"Project: {project_id}")

# Try different regions
regions = ["us-central1", "us-east1", "us-west1"]

for region in regions:
    try:
        print(f"\nTrying region: {region}")
        vertexai.init(project=project_id, location=region)
        
        # Try different model names
        models = ["gemini-1.0-pro", "gemini-1.5-pro", "gemini-1.5-flash"]
        
        for model_name in models:
            try:
                from vertexai.generative_models import GenerativeModel
                model = GenerativeModel(model_name)
                response = model.generate_content("Hello")
                print(f"✓ {model_name} works in {region}")
                break
            except Exception as e:
                print(f"✗ {model_name}: {str(e)[:100]}...")
                
    except Exception as e:
        print(f"✗ Region {region} failed: {e}")