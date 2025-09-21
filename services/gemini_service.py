import vertexai
from vertexai.generative_models import GenerativeModel
import json
import os

def generate_roadmap(learning_summary):
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise Exception("GOOGLE_CLOUD_PROJECT not configured")
        
    vertexai.init(project=project_id, location="us-central1")
    
    model = GenerativeModel("gemini-2.5-flash-lite")
    
    prompt = f"""
    Create a detailed learning roadmap based on this summary: {learning_summary}
    
    Return ONLY valid JSON in this format:
    {{
        "topic": "extract topic name from summary",
        "summary": "Brief overview of the roadmap covering main topics and goals",
        "days": [
            {{
                "day": 1,
                "title": "Day 1 title",
                "tasks": ["task1", "task2"],
                "lesson": "Detailed lesson content for audio conversion"
            }}
        ]
    }}
    Learning Summary: "{learning_summary}"
    """
    
    response = model.generate_content(prompt)
    
    print(f"[GEMINI] Raw response: {response.text}")
    
    # Clean the response text
    response_text = response.text.strip()
    
    # Remove markdown code blocks if present
    if response_text.startswith('```json'):
        response_text = response_text[7:]
    if response_text.startswith('```'):
        response_text = response_text[3:]
    if response_text.endswith('```'):
        response_text = response_text[:-3]
    
    response_text = response_text.strip()
    print(f"[GEMINI] Cleaned response: {response_text}")
    
    try:
        if not response_text:
            raise Exception("Empty response from Gemini")
        return json.loads(response_text)
    except json.JSONDecodeError as e:
        print(f"[GEMINI] JSON decode error: {e}")
        print(f"[GEMINI] Failed text: {response_text}")
        # Return a fallback roadmap structure
        return {
            "topic": "Learning Topic",
            "summary": "A comprehensive learning roadmap to help you master your chosen subject.",
            "days": [
                {
                    "day": 1,
                    "title": "Getting Started",
                    "tasks": ["Introduction to the topic", "Basic concepts"],
                    "lesson": "Welcome to your learning journey! Today we'll start with the fundamentals and build a strong foundation."
                }
            ]
        }

def get_gemini_response(prompt):
    """Get a simple text response from Gemini for conversation"""
    try:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            return "I'm having trouble connecting. Could you please repeat that?"
            
        vertexai.init(project=project_id, location="us-central1")
        
        model = GenerativeModel("gemini-2.5-flash-lite")
        response = model.generate_content(prompt)
        
        if not response or not response.text:
            return "I'm having trouble understanding. Could you please repeat that?"
            
        return response.text.strip()
    except Exception as e:
        print(f"[GEMINI] Error getting response: {e}")
        return "I'm having trouble understanding. Could you please repeat that?"