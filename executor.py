import pyautogui
import pyperclip
import time
import config

def execute_prompt_in_ide(prompt_text, cursor_pos=None):
    if not prompt_text or prompt_text.startswith("ERROR"):
        print("⏭️ Skipping execution due to empty/error prompt.")
        if prompt_text:
            print(prompt_text)
        return
        
    print(f"🚀 Taking control of IDE to execute prompt...")
    print(f"💬 Prompt: {prompt_text}")
    
    # 1. Click the screen to ensure the IDE has window focus
    if cursor_pos:
        print(f"DEBUG: Clicking at {cursor_pos} to ensure window focus...")
        original_pos = pyautogui.position()
        pyautogui.click(x=cursor_pos[0], y=cursor_pos[1])
        # Move mouse back out of the way
        pyautogui.moveTo(original_pos)
        time.sleep(0.5)
    else:
        print("DEBUG: No cursor_pos provided, hoping IDE has focus...")
    
    # 2. Trigger IDE Chat Shortcut
    print(f"DEBUG: ⌨️  Pressing shortcut: {config.IDE_CHAT_SHORTCUT}")
    
    # macOS sometimes drops `hotkey` modifiers, so we hold them explicitly
    modifiers = config.IDE_CHAT_SHORTCUT[:-1]
    main_key = config.IDE_CHAT_SHORTCUT[-1]
    
    for mod in modifiers:
        mod_key = 'command' if mod == 'cmd' else mod
        pyautogui.keyDown(mod_key)
        
    pyautogui.press(main_key)
    
    for mod in reversed(modifiers):
        mod_key = 'command' if mod == 'cmd' else mod
        pyautogui.keyUp(mod_key)
    print("DEBUG: Waiting 1.5s for chat input to gain focus...")
    time.sleep(1.5) # Time for chat input to gain focus (increased for electron apps)
    
    # 3. Type the text explicitly (bypassing clipboard issues entirely)
    print("DEBUG: ⌨️  TYPING out the prompt directly character-by-character...")
    # interval=0.01 makes it slightly faster than instant pasting, but slow enough to be reliable
    pyautogui.write(prompt_text, interval=0.01)
    
    # Wait a moment for UI to register the typing before hitting Enter
    time.sleep(0.5)
    
    # 4. Press Enter to submit
    print("DEBUG: Pressing 'enter' to submit...")
    pyautogui.press('enter')
    print("✅ Successfully submitted to AI Agent!")

def execute_custom_command(command_name, cursor_pos=None):
    print(f"🚀 Executing custom action: {command_name}")
    if command_name == "write_code":
        # Simulate 'cmd+l' to focus Cursor/IDE chat
        execute_prompt_in_ide("", cursor_pos)
        print("✅ Focus triggered for Cursor.")
    else:
        print(f"⚠️ Unknown command: {command_name}")
