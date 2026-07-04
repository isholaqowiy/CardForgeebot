import os
import qrcode
from config import TEMP_DIR

def generate_vcard_qr(data: dict, user_id: int) -> str:
    """Compiles valid structured vCard fields into a scannable structural visual QR graphic matrix asset."""
    vcard_str = (
        "BEGIN:VCARD\n"
        "VERSION:3.0\n"
        f"FN:{data.get('name', '')}\n"
        f"ORG:{data.get('company', '')}\n"
        f"TITLE:{data.get('title', '')}\n"
        f"TEL;TYPE=CELL:{data.get('phone', '')}\n"
        f"EMAIL:{data.get('email', '')}\n"
        f"URL:{data.get('website', '')}\n"
        "END:VCARD"
    )
    
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(vcard_str)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    output_path = os.path.join(TEMP_DIR, f"qr_{user_id}.png")
    img.save(output_path)
    return output_path

