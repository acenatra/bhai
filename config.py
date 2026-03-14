import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

# Action Triggers
# The hotkey to press and hold to start recording voice.
# Mac default: command + shift + space
RECORDING_HOTKEY = '<cmd>+<shift>+<space>'

# The keyboard shortcut to focus your IDE's AI chat input.
# Mac typical: command + l
IDE_CHAT_SHORTCUT = ['cmd', 'l']

# Other configuration
TARGET_CIRCLE_RADIUS = 30
TARGET_CIRCLE_COLOR = (255, 0, 0)
TARGET_CIRCLE_THICKNESS = 5
