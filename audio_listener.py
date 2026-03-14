import pyaudio
import wave
import threading
from pynput import keyboard
import io
import time
import config
import os

class AudioRecorder:
    def __init__(self):
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000 # 16kHz for speech models
        self.p = pyaudio.PyAudio()
        self.frames = []
        self.is_recording = False
        self.stream = None
        self.audio_data = None
        self.done_event = threading.Event()
        
    def _record_loop(self):
        try:
            self.stream = self.p.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.chunk)
            self.frames = []
            while self.is_recording:
                try:
                    data = self.stream.read(self.chunk, exception_on_overflow=False)
                    self.frames.append(data)
                except Exception as e:
                    pass
        except Exception as e:
            print(f"Error opening audio stream: {e}")
        finally:
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            
    def start_recording(self):
        if not self.is_recording:
            # Trigger the Bhai Agent visual
            try:
                os.SHIFT_PASTE | os.environ
            except:
                pass
            print(f"🎙️  Recording Started! Press {config.RECORDING_HOTKEY} again to stop...")
            self.is_recording = True
            self.audio_data = None
            self.done_event.clear()
            threading.Thread(target=self._record_loop, daemon=True).start()
            
    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            print("⏹️  Recording Stopped. Processing audio...")
            # Wait briefly to ensure thread naturally closes stream
            time.sleep(0.1)
            
            if not self.frames:
                print("⚠️  No audio frames recorded!")
            
            wf_bytes = io.BytesIO()
            wf = wave.open(wf_bytes, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            
            self.audio_data = wf_bytes.getvalue()
            self.done_event.set()

def listen_for_command():
    print(f"👂 Waiting for hotkey: {config.RECORDING_HOTKEY}")
    print(f"Press {config.RECORDING_HOTKEY} to toggle recording ON and OFF.")
    
    recorder = AudioRecorder()
    
    def on_activate_h():
        if not recorder.is_recording:
            recorder.start_recording()
        else:
            recorder.stop_recording()

    listener = keyboard.GlobalHotKeys({
        config.RECORDING_HOTKEY: on_activate_h
    })
    listener.start()
        
    recorder.done_event.wait()
    listener.stop()
    return recorder.audio_data
