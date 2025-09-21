from typing import Dict, List, Optional
import uuid
from datetime import datetime
from .firestore_service import db, save_welcome_session as save_session_to_db
from .gemini_service import generate_roadmap, get_gemini_response
from .tts_service import generate_audio

class WelcomeSession:
    def __init__(self, guest_id: str):
        self.guest_id = guest_id
        self.session_name = "welcome_session"
        self.chat_history = []
        self.collected_info = {
            "topic": None,
            "days": None,
            "experience_level": None,
            "ready_to_generate": False,
            "info_complete": False,
            "confirmation_asked": False
        }
        self.current_step = "topic"

    def add_message(self, role: str, content: str, audio_url: str = None):
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "audio_url": audio_url
        }
        self.chat_history.append(message)

    def process_user_input(self, user_input: str) -> Dict:
        """Process user input using Gemini AI for all responses"""
        from .gemini_service import get_gemini_response
        
        # First, extract information from user input
        self._extract_info_from_user_input(user_input)
        
        # Create comprehensive context with chat history for Gemini
        context = f"""
You are a learning assistant for blind users. You need to collect:
1. Topic they want to learn
2. Number of days (7-30)
3. Experience level
4. Final confirmation

Current progress:
- Topic: {self.collected_info.get('topic', 'Not collected')}
- Days: {self.collected_info.get('days', 'Not collected')}
- Experience: {self.collected_info.get('experience_level', 'Not collected')}
- Info Complete: {self.collected_info.get('info_complete', False)}
- Confirmation Asked: {self.collected_info.get('confirmation_asked', False)}

Conversation history:
{self._get_chat_context()}

User just said: "{user_input}"

Instructions:
- This is for a blind user - always end with "Press Enter to record your response."
- Don't repeat questions you already asked
- Move to next step based on what you've collected
- If you have topic, days, and experience, ask if they want to add anything else
- Keep responses under 50 words
- Be conversational and encouraging

Just respond naturally to their confirmation.

Respond naturally based on the conversation flow:
"""
        
        # Get response from Gemini
        response_text = get_gemini_response(context)
        
        # Simple logic: if info is complete and confirmation was asked, set ready to generate
        if self.collected_info.get('info_complete') and self.collected_info.get('confirmation_asked'):
            self.collected_info['ready_to_generate'] = True

        try:
            # Generate audio for response
            audio_path = generate_audio(response_text)
            audio_url = f"/audio/{audio_path.split('/')[-1]}"
            
            # Add messages to chat history
            self.add_message("user", user_input)
            self.add_message("assistant", response_text, audio_url)
            
            # Generate summary if info is complete (even if not ready to generate yet)
            summary = None
            if self.collected_info["info_complete"] or self.collected_info["ready_to_generate"]:
                summary = self._generate_learning_summary()
            
            return {
                "response": response_text,
                "audio_url": audio_url,
                "ready_to_generate": self.collected_info["ready_to_generate"],
                "learning_summary": summary,
                "collected_info": self.collected_info,
                "current_step": self.current_step
            }
        except Exception as e:
            print(f"Error in process_user_input: {e}")
            # Fallback response
            response_text = "I'm having trouble understanding. Could you please repeat that?"
            audio_path = generate_audio(response_text)
            audio_url = f"/audio/{audio_path.split('/')[-1]}"
            
            return {
                "response": response_text,
                "audio_url": audio_url,
                "ready_to_generate": False,
                "learning_summary": None,
                "collected_info": self.collected_info,
                "current_step": self.current_step
            }
    
    def _extract_info_from_user_input(self, user_input: str):
        """Extract information from user input and update state"""
        # Extract topic if not collected
        if not self.collected_info.get('topic'):
            if not (user_input.lower() in ['wooooo', 'woo', 'hello', 'hi', 'hey'] or len(user_input.strip()) < 3):
                self.collected_info['topic'] = user_input.strip()
                self.current_step = 'days'
        
        # Extract days if not collected
        elif not self.collected_info.get('days'):
            import re
            numbers = re.findall(r'\d+', user_input)
            if numbers:
                days = int(numbers[0])
                if 7 <= days <= 30:
                    self.collected_info['days'] = days
                    self.current_step = 'experience'
        
        # Extract experience if not collected
        elif not self.collected_info.get('experience_level'):
            user_lower = user_input.lower()
            if any(word in user_lower for word in ['beginner', 'new', 'start', 'never', 'first']):
                experience = 'beginner'
            elif any(word in user_lower for word in ['intermediate', 'some', 'basic', 'little']):
                experience = 'intermediate'
            elif any(word in user_lower for word in ['advanced', 'expert', 'experienced', 'good']):
                experience = 'advanced'
            else:
                experience = user_input.strip()
            
            self.collected_info['experience_level'] = experience
            self.collected_info['info_complete'] = True
        
        # Handle confirmation response
        elif self.collected_info.get('info_complete') and not self.collected_info.get('confirmation_asked'):
            self.collected_info['confirmation_asked'] = True
    
    def _generate_learning_summary(self) -> str:
        """Generate a summary of collected learning information"""
        from .gemini_service import get_gemini_response
        
        context = f"""
Generate a brief learning summary based on this information:
- Topic: {self.collected_info['topic']}
- Duration: {self.collected_info['days']} days
- Experience Level: {self.collected_info['experience_level']}

Create a 2-3 sentence summary of what the user wants to learn. 
Make it sound professional and clear. Keep it under 50 words.
"""
        
        try:
            return get_gemini_response(context)
        except:
            return f"Learn {self.collected_info['topic']} in {self.collected_info['days']} days with {self.collected_info['experience_level']} level experience."
    
    def _get_chat_context(self) -> str:
        """Get recent chat history for context"""
        if not self.chat_history:
            return "No previous conversation"
        
        recent_messages = self.chat_history[-6:] if len(self.chat_history) > 6 else self.chat_history
        context = ""
        for msg in recent_messages:
            # Clean the content to remove "Press Enter" instructions for context
            clean_content = msg['content'].replace("Press Enter to record your response.", "").strip()
            context += f"{msg['role']}: {clean_content}\n"
        return context
    


# In-memory session storage
welcome_sessions: Dict[str, WelcomeSession] = {}

def create_welcome_session():
    """Create a new welcome session with Gemini-generated welcome message"""
    from .gemini_service import get_gemini_response
    from .tts_service import generate_audio
    
    guest_id = str(uuid.uuid4())
    session = WelcomeSession(guest_id)
    
    # Get welcome message from Gemini
    welcome_prompt = """
You are a friendly learning assistant for Vision Path designed for blind users. A new user just arrived. 
Greet them warmly and ask what they would like to learn today. 
Mention that they should press Enter to start recording their response after you finish speaking.
Be enthusiastic and encouraging. Keep it under 40 words.
Don't mention days or experience level yet - just focus on what they want to learn.
"""
    
    welcome_message = get_gemini_response(welcome_prompt)
    
    # Generate audio for welcome message
    audio_path = generate_audio(welcome_message)
    audio_url = f"/audio/{audio_path.split('/')[-1]}"
    
    # Add welcome message to chat history
    session.add_message("assistant", welcome_message, audio_url)
    
    welcome_sessions[guest_id] = session
    
    # Save to database (optional)
    try:
        save_session_to_db(
            guest_id,
            session.session_name,
            session.chat_history,
            session.collected_info,
            session.current_step
        )
    except Exception as e:
        print(f"[WARNING] Database save failed, continuing with in-memory storage: {e}")
    
    return guest_id, welcome_message, audio_url

def get_welcome_session(guest_id: str) -> Optional[WelcomeSession]:
    """Get existing welcome session"""
    return welcome_sessions.get(guest_id)

def save_welcome_session(session: WelcomeSession):
    """Save session to database"""
    try:
        save_session_to_db(
            session.guest_id,
            session.session_name,
            session.chat_history,
            session.collected_info,
            session.current_step
        )
    except Exception as e:
        print(f"[WARNING] Database save failed, continuing with in-memory storage: {e}")

def process_welcome_input(guest_id: str, user_input: str) -> Dict:
    """Process user input in welcome session"""
    session = get_welcome_session(guest_id)
    if not session:
        raise Exception("Welcome session not found")
    
    result = session.process_user_input(user_input)
    save_welcome_session(session)
    
    return result

def generate_roadmap_from_session(guest_id: str) -> Dict:
    """Generate roadmap from collected session info"""
    session = get_welcome_session(guest_id)
    if not session or not session.collected_info["ready_to_generate"]:
        raise Exception("Session not ready for roadmap generation")
    
    # Create detailed prompt from collected info
    prompt = f"""Create a {session.collected_info['days']}-day learning roadmap for {session.collected_info['topic']}. 
    The learner has {session.collected_info['experience_level']} experience level. 
    Make it practical and progressive."""
    
    roadmap_json = generate_roadmap(prompt)
    return roadmap_json