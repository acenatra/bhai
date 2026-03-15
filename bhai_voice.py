import pyttsx3
import threading
import os
import subprocess

class BhaiVoice:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 170)
            self.engine.setProperty('volume', 1.0)
        except Exception as e:
            print(f"⚠️ pyttsx3 init failed: {e}")
            self.engine = None

    def speak(self, text):
        if not text:
            return

        def run_native_say():
            # macOS 'say' command is excellent at auto-detecting language (Hindi, Urdu, English, etc.)
            try:
                subprocess.run(["say", text])
            except:
                print(f"🤖 Bhai says (text): {text}")

        def run_pyttsx3():
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except:
                run_native_say()

        # Prefer native macOS 'say' for multi-lingual quality, fallback to pyttsx3
        threading.Thread(target=run_native_say, daemon=True).start()

bhai_voice = BhaiVoice()

if __name__ == "__main__":
    print("Testing Bhai's multi-lingual voice...")
    bhai_voice.speak("Hello! नमस्ते! آپ کیسے ہیں؟")
    import time
    time.sleep(3)
