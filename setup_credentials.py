import os
import shutil

def setup_credentials():
    """Helper script to set up credentials for the project"""
    
    print("🔧 Voice Learning Tutor - Credential Setup")
    print("=" * 50)
    
    # Check if .env exists
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            shutil.copy('.env.example', '.env')
            print("✓ Created .env file from .env.example")
        else:
            print("❌ .env.example not found")
            return
    
    # Check for credentials file
    env_file = '.env'
    with open(env_file, 'r') as f:
        content = f.read()
    
    if 'your-project-id' in content or 'path/to/your' in content:
        print("\n⚠️  Please update your .env file with:")
        print("1. Your GCP project ID")
        print("2. Path to your service account JSON file")
        print("\nExample:")
        print("GOOGLE_APPLICATION_CREDENTIALS=./my-service-account.json")
        print("GOOGLE_CLOUD_PROJECT=my-project-123")
    else:
        print("✓ .env file appears to be configured")
    
    print("\n📋 Next steps:")
    print("1. Download your service account JSON from GCP Console")
    print("2. Place it in the project root directory")
    print("3. Update GOOGLE_APPLICATION_CREDENTIALS in .env")
    print("4. Run: python main.py")

if __name__ == "__main__":
    setup_credentials()