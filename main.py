import screen_context
import audio_listener
import ai_brain
import executor
import time

def main():
    print("========================================")
    print("🤖 Voice-to-Code Orchestrator Started")
    print("========================================")
    
    while True:
        try:
            # 1. Wait for and record audio
            audio_bytes = audio_listener.listen_for_command()
            
            if not audio_bytes:
                print("No audio captured. Resuming...")
                continue
                
            # 2. Capture screen state immediately upon recording finish
            print("📸 Capturing screen context...")
            image_bytes, cursor_pos = screen_context.capture_screen_with_cursor()
            
            # 3. Send to Gemini to generate the prompt
            prompt = ai_brain.generate_orchestrator_prompt(image_bytes, audio_bytes)
            
            # 4. Emulate keystrokes to IDE
            executor.execute_prompt_in_ide(prompt, cursor_pos)
            print("\n----------------------------------------\nReady for next command...\n")
            
        except KeyboardInterrupt:
            print("\n👋 Exiting Voice-to-Code Orchestrator...")
            break
        except Exception as e:
            print(f"⚠️ Unexpected error in main loop: {e}")
            time.sleep(1) # prevent rapid looping on error

if __name__ == "__main__":
    main()
