from flask import Flask, render_template
import qrcode
from io import BytesIO
from base64 import b64encode

app = Flask(__name__)

@app.route('/')
def index():
    # Create the QRCode object
    qr = qrcode.QRCode()
    
    # Add data to the QR code
    qr.add_data("https://www.supermarket-checkin.com")
    qr.make(fit=True)
    
    # Generate the QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save it to a buffer to render in the HTML
    buffer = BytesIO()
    img.save(buffer)
    qr_code_base64 = b64encode(buffer.getvalue()).decode('utf-8')
    
    return render_template('index.html', qr_code_base64=qr_code_base64)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
