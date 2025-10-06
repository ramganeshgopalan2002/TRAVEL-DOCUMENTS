from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import qrcode
import barcode
from barcode.writer import ImageWriter
import os
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)

# Use a relative path for the images folder, located inside the app's root directory.
# This makes the application portable and avoids permission errors.
IMAGES_FOLDER = 'images'
BASE_URL = '/'  # Use a relative base URL

# Ensure the images folder exists, creating it if necessary
# This will create the 'images' folder in the same directory as this script.
os.makedirs(os.path.join(app.root_path, IMAGES_FOLDER), exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'success': True,
        'message': 'Travel Document Generator API is running'
    })

@app.route('/api/generate/qr-code', methods=['POST'])
def generate_qr_code():
    try:
        data = request.json or {}
        first_name = data.get('firstName', 'John')
        last_name = data.get('lastName', 'Doe')
        flight = data.get('flight', 'PH 0121')
        from_airport = data.get('from', 'BOM')
        to_airport = data.get('to', 'DEL')
        date = data.get('date', '2025-09-10')
        time = data.get('time', '13:15')
        seat = data.get('seat', '14A')
        gate = data.get('gate', 'B12')
        pnr = data.get('pnr', 'ABC123')

        qr_data = f"BOARDING PASS\nPassenger: {first_name} {last_name}\nFlight: {flight}\nFrom: {from_airport}\nTo: {to_airport}\nDate: {date}\nTime: {time}\nSeat: {seat}\nGate: {gate}\nPNR: {pnr}"

        # Generate QR code
        qr_img = qrcode.make(qr_data)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"qr_code_{timestamp}_{unique_id}.png"
        
        # Construct the full file path using the application's root path
        filepath = os.path.join(app.root_path, IMAGES_FOLDER, filename)
        
        # Save QR code to file
        qr_img.save(filepath)
        
        # Generate the full URL for the generated image
        image_url = f"{BASE_URL}{IMAGES_FOLDER}/{filename}"

        return jsonify({
            'success': True,
            'data': {
                'passengerName': f"{first_name} {last_name}".upper(),
                'flight': flight,
                'fromAirport': from_airport,
                'toAirport': to_airport,
                'date': date,
                'time': time,
                'seat': seat,
                'gate': gate,
                'pnr': pnr,
                'qrImageUrl': image_url,
                'filename': filename
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/generate/barcode', methods=['POST'])
def generate_barcode():
    try:
        data = request.json or {}
        first_name = data.get('firstName', 'John')
        last_name = data.get('lastName', 'Doe')
        flight = data.get('flight', 'PH 0121')
        from_airport = data.get('from', 'BOM')
        to_airport = data.get('to', 'DEL')
        date = data.get('date', '2025-09-10')
        time = data.get('time', '13:15')
        seat = data.get('seat', '14A')
        gate = data.get('gate', 'B12')
        pnr = data.get('pnr', 'ABC123')

        # Create barcode data (using PNR as barcode content)
        barcode_data = pnr
        
        # Generate barcode (using Code128 format)
        barcode_class = barcode.get_barcode_class('code128')
        barcode_img = barcode_class(barcode_data, writer=ImageWriter())
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"barcode_{timestamp}_{unique_id}.png"
        
        # Construct the full file path using the application's root path
        filepath = os.path.join(app.root_path, IMAGES_FOLDER, filename)
        
        # Save barcode to file
        barcode_img.save(filepath)
        
        # Generate the full URL for the generated image
        image_url = f"{BASE_URL}{IMAGES_FOLDER}/{filename}"

        return jsonify({
            'success': True,
            'data': {
                'passengerName': f"{first_name} {last_name}".upper(),
                'flight': flight,
                'fromAirport': from_airport,
                'toAirport': to_airport,
                'date': date,
                'time': time,
                'seat': seat,
                'gate': gate,
                'pnr': pnr,
                'barcodeImageUrl': image_url,
                'filename': filename
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Add a route to serve the images from the 'images' directory
@app.route(f'/{IMAGES_FOLDER}/<filename>')
def serve_image(filename):
    try:
        return send_from_directory(os.path.join(app.root_path, IMAGES_FOLDER), filename)
    except Exception as e:
        return jsonify({'error': 'Image not found', 'details': str(e)}), 404

if __name__ == '__main__':
    # Flask will automatically serve files from the 'static' folder.
    # We are using send_from_directory for our custom 'images' folder.
    # app.static_folder = IMAGES_FOLDER is not needed.
    app.run(debug=True, host='0.0.0.0', port=5000)
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import qrcode
import base64
from io import BytesIO
import barcode
from barcode.writer import ImageWriter

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Helper function to generate QR code and return a base64 string
def generate_qr_code(data_string):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data_string)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{img_str}"

# Helper function to generate barcode and return a base64 string
def generate_barcode(data_string):
    try:
        # Use a standard format like Code128
        Code128 = barcode.get_barcode_class('code128')
        code = Code128(data_string, writer=ImageWriter())
        
        buffered = BytesIO()
        # Save the barcode to the buffer
        code.write(buffered, options={"module_width": 0.2, "module_height": 10, "font_size": 10})
        
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        # Return an error or a placeholder image if the data is invalid for the barcode type
        print(f"Error generating barcode: {e}")
        return None

# Route to serve the HTML file
@app.route('/')
def serve_html():
    return send_from_directory('.', 'new.html')

# API route to generate QR code
@app.route('/api/generate/qr-code', methods=['POST'])
def handle_qr_code_generation():
    data = request.json
    try:
        data_string = str(data)  # Convert the JSON data to a string for the QR code
        qr_image_url = generate_qr_code(data_string)
        return jsonify({'success': True, 'data': {'qrImageUrl': qr_image_url}})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# API route to generate barcode
@app.route('/api/generate/barcode', methods=['POST'])
def handle_barcode_generation():
    data = request.json
    try:
        data_string = data.get('pnr') or data.get('bagNumber') or 'Default'
        barcode_image_url = generate_barcode(data_string)
        if barcode_image_url:
            return jsonify({'success': True, 'data': {'barcodeImageUrl': barcode_image_url}})
        else:
            return jsonify({'success': False, 'error': 'Failed to generate barcode from data'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    # You need to install Flask, qrcode, and python-barcode first:
    # pip install Flask qrcode python-barcode[svg]
    app.run(debug=True)
