import os
import json
from google.oauth2 import service_account

def get_credentials():
    """Get Google Cloud credentials from environment variables or file."""
    
    # Try JSON credentials from environment variable first (for Railway)
    creds_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    if creds_json:
        try:
            creds_dict = json.loads(creds_json)
            return service_account.Credentials.from_service_account_info(creds_dict)
        except json.JSONDecodeError:
            print("[AUTH] Invalid JSON in GOOGLE_APPLICATION_CREDENTIALS_JSON")
    
    # Fallback to file path (for local development)
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if creds_path and os.path.exists(creds_path):
        return service_account.Credentials.from_service_account_file(creds_path)
    
    # Use default credentials (will fail in Railway without setup)
    return None