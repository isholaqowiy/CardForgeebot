import os
from PIL import Image, ImageDraw, ImageFont
from config import TEMP_DIR
import qr_generator

def render_business_card(data: dict, user_id: int) -> str:
    """Generates a high-resolution, pixel-perfect physical image print of a business card matrix layout asset."""
    # Production card dimensions canvas
    width, height = 1050, 600
    
    # Establish default color scheme frameworks based on selected layout definitions
    bg_color = "#111111" if data.get('template') == "Dark Theme" else "#FFFFFF"
    text_color = "#FFFFFF" if data.get('template') == "Dark Theme" else "#222222"
    accent_color = "#007AFF"
    
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Use fallback default font layers
    try:
        font_name = ImageFont.load_default()
        font_title = ImageFont.load_default()
    except IOError:
        font_name = ImageFont.load_default()
        font_title = ImageFont.load_default()
        
    # Draw text information layers
    draw.text((60, 80), data.get('name', 'Full Name'), fill=accent_color, font=font_name)
    draw.text((60, 150), data.get('title', 'Job Title'), fill=text_color, font=font_title)
    draw.text((60, 200), data.get('company', 'Company Name'), fill=text_color, font=font_title)
    
    draw.text((60, 400), f"📞 {data.get('phone', '')}", fill=text_color, font=font_title)
    draw.text((60, 450), f"✉️ {data.get('email', '')}", fill=text_color, font=font_title)
    draw.text((60, 500), f"🌐 {data.get('website', '')}", fill=text_color, font=font_title)
    
    # Render and combine nested structural QR elements path
    qr_path = qr_generator.generate_vcard_qr(data, user_id)
    if os.path.exists(qr_path):
        with Image.open(qr_path) as qr_img:
            qr_resized = qr_img.resize((280, 280))
            img.paste(qr_resized, (700, 160))
        try:
            os.remove(qr_path)
        except Exception:
            pass
            
    output_path = os.path.join(TEMP_DIR, f"card_{user_id}.png")
    img.save(output_path, quality=100)
    return output_path

