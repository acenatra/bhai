import base64
import config
from groq import Groq
from openai import OpenAI

SYSTEM_PROMPT = """You are an AI coding orchestrator designed to be the interface between a programmer and their coding agent.
You are given two inputs:
1. An image of the user's screen. A bright RED CIRCLE has been drawn on the screen indicating EXACTLY where their mouse cursor is pointing.
2. A voice recording of the user stating a command or asking a question about the code they are pointing at.

YOUR INSTRUCTIONS:
Understand the user's voice command and analyze the code around the RED CIRCLE.
Produce a refined, standalone TEXT PROMPT that will be automatically inserted into the user's coding agent chat box (e.g., Cursor, Antigravity).

The output text you generate must be the RAW PROMPT. Do NOT include phrases like "Here is the prompt for your coding agent:". 
Just output the prompt text directly. Your output should clearly mention the function Name, class name, or specific files to help the coding agent know exactly what to edit.
For example, if the user points at 'def calculate_tax()' and says "Make this more readable", your output should literally be something like: "Please make the `calculate_tax` function more readable and well-documented."
"""

def init_groq():
    if not config.GROQ_API_KEY or config.GROQ_API_KEY == "your_free_groq_api_key_here":
        print("⚠️ Warning: GROQ_API_KEY is missing or invalid in .env file.")
        return None
    return Groq(api_key=config.GROQ_API_KEY)

def init_github_models():
    if not config.GITHUB_TOKEN or config.GITHUB_TOKEN == "your_free_github_personal_access_token_here":
        print("⚠️ Warning: GITHUB_TOKEN is missing or invalid in .env file.")
        return None
    return OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=config.GITHUB_TOKEN,
    )

groq_client = init_groq()
github_client = init_github_models()

def generate_orchestrator_prompt(image_bytes, audio_bytes):
    if not groq_client or not github_client:
        return "ERROR: AI clients not fully initialized. Please set GROQ_API_KEY and GITHUB_TOKEN in the .env file."
        
    print("🧠 Processing with Groq & GitHub Models...")
    try:
        # 1. Transcribe audio using Whisper on Groq
        print("   -> Transcribing audio with Groq...")
        transcription = groq_client.audio.transcriptions.create(
            file=("audio.wav", audio_bytes),
            model="whisper-large-v3-turbo",
            response_format="text",
        )
        user_spoken_text = transcription.strip()
        print(f"   -> Heard: '{user_spoken_text}'")
        
        # 2. Convert image to base64
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        image_url = f"data:image/png;base64,{base64_image}"
        
        # 3. Call Vision Model (gpt-4o) using GitHub Models
        print("   -> Analyzing image and generating prompt with GitHub Models...")
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Listen to the audio command: '{user_spoken_text}'. Now look at the image where the cursor is pointing. Give me the final prompt to feed the coding agent."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ]
        
        response = github_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.2,
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Error communicating with AI: {e}")
        return f"ERROR: {e}"
