import screen_context
import audio_listener
import ai_brain
import executor
import bhai_voice
import web_bhai
import time
import json

def main():
    print("========================================")
    print("🤖 Bhai 2.0: Multi-lingual AI Companion")
    print("========================================")
    
    bhai_voice.bhai_voice.speak("System online. Bhai is ready to chat!")
    
    while True:
        try:
            # 1. Listen for voice
            audio_bytes = audio_listener.listen_for_command()
            
            if not audio_bytes:
                continue
                
            # 2. Capture screen state
            print("📸 Capturing screen...")
            image_bytes, cursor_pos = screen_context.capture_screen_with_cursor()
            
            # 3. Think (Multilingual Response)
            print("🧠 Thinking...")
            decision = ai_brain.generate_orchestrator_action(image_bytes, audio_bytes)
            
            # 4. Speak response IMMEDIATELY
            voice_text = decision.get("voice_response")
            if voice_text:
                print(f"🤖 Bhai: {voice_text}")
                bhai_voice.bhai_voice.speak(voice_text)
            
            # 5. Route Action (Only if explicitly requested)
            action = decision.get("action")
            params = decision.get("parameters", {})
            
            if action == "ide_automate":
                print(f"🎬 Performing action: {action}")
                executor.execute_prompt_in_ide(params.get("prompt"), cursor_pos)
            elif action == "web_browse" or action == "play_youtube":
                print(f"🎬 Performing action: {action}")
                web_bhai.run_web_action(action, params)
            elif action == "execute_custom":
                print(f"🎬 Performing action: {action}")
                executor.execute_custom_command(params.get("command"), cursor_pos)
            
            print("\n----------------------------------------\nReady for next command...\n")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
