import mss
import pyautogui
from PIL import Image, ImageDraw
import io
import config

def capture_screen_with_cursor():
    """Captures the screen and draws a red circle at the mouse cursor."""
    with mss.mss() as sct:
        # Get the primary monitor
        monitor = sct.monitors[1]
        
        # Capture screen as BGRA
        sct_img = sct.grab(monitor)
        
        # Convert to PIL Image
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        
        # Get mouse absolute position
        x, y = pyautogui.position()
        
        # Adjust coordinate to image space. 
        # `monitor["left"]` and `monitor["top"]` represent the offset of the primary monitor in absolute coords.
        # But usually primary monitor offset is 0,0 anyway.
        img_x = x - monitor["left"]
        img_y = y - monitor["top"]
        
        draw = ImageDraw.Draw(img)
        radius = config.TARGET_CIRCLE_RADIUS
        
        # Draw the target circle
        left_up_point = (img_x - radius, img_y - radius)
        right_down_point = (img_x + radius, img_y + radius)
        
        draw.ellipse([left_up_point, right_down_point], 
                     outline=config.TARGET_CIRCLE_COLOR, 
                     width=config.TARGET_CIRCLE_THICKNESS)
                     
        # Save to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return img_byte_arr.getvalue(), (x, y)
