import base64
import json
import config
from groq import Groq
from openai import OpenAI

SYSTEM_PROMPT = """You are 'Bhai', a helpful and intelligent AI companion.
You can see the user's screen and hear their voice commands in various languages (English, Hindi, Urdu, etc.).

YOUR CORE RULES:
1. RESPOND IN THE SAME LANGUAGE: If the user speaks in Hindi, you must respond in Hindi. If Urdu, respond in Urdu.
2. BE CONVERSATIONAL: Focus on speaking the response back to the user clearly.
3. ACTIONS ONLY WHEN EXPLICITLY ASKED: Do not trigger browser or IDE actions unless the user clearly says something like "Bhai, search for X" or "Bhai, perform this action".
4. OUTPUT FORMAT: You must return a valid JSON object ONLY.

JSON SCHEMA:
{
  "voice_response": "The spoken response in the SAME LANGUAGE as the user's query.",
  "action": "web_browse | play_youtube | ide_automate | speak_only | execute_custom",
  "parameters": {
    "url": "optional (for web_browse)",
    "query": "optional (search query for web_browse or song name for play_youtube)",
    "prompt": "refined coding prompt if action is ide_automate",
    "command": "custom command if needed"
  }
}

If the user asks a general question like "This function what it does?", set action to "speak_only" and provide a clear explanation in their language.
"""

def init_groq():
    if not config.GROQ_API_KEY or config.GROQ_API_KEY == "your_free_groq_api_key_here":
        return None
    return Groq(api_key=config.GROQ_API_KEY)

def init_github_models():
    if not config.GITHUB_TOKEN or config.GITHUB_TOKEN == "your_free_github_personal_access_token_here":
        return None
    return OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=config.GITHUB_TOKEN,
    )

groq_client = init_groq()
github_client = init_github_models()

def generate_orchestrator_action(image_bytes, audio_bytes):
    if not groq_client or not github_client:
        return {
            "action": "speak_only",
            "voice_response": "AI clients not initialized. Check .env."
        }
        
    try:
        # 1. Transcribe audio (Whisper handles multi-lingual transcription very well)
        transcription = groq_client.audio.transcriptions.create(
            file=("audio.wav", audio_bytes),
            model="whisper-large-v3-turbo",
            response_format="text",
        )
        user_spoken_text = transcription.strip()
        print(f"   -> Bhai heard: '{user_spoken_text}'")
        
        # 2. Vision analysis & Decision
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        image_url = f"data:image/png;base64,{base64_image}"
        
        response = github_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": [
                    {"type": "text", "text": f"User's spoken query: '{user_spoken_text}'. (Respond in the same language as the query)"},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]}
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
        )
        
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"❌ Brain Error: {e}")
        return {
            "action": "speak_only",
            "voice_response": f"Error: {str(e)}"
        }
