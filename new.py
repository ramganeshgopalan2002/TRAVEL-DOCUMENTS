from flask import Flask, render_template, request, jsonify
import qrcode
import barcode
from barcode.writer import ImageWriter
import os
from datetime import datetime
import uuid

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

IMAGES_FOLDER = '/home/local/CORPORATE/ramganesh.gopalan/Desktop/Final pass/Boarding_pass/images'
BASE_URL = 'http://localhost:5000'

os.makedirs(IMAGES_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('qr.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'success': True, 'message': 'API is running'})

@app.route('/api/generate/qr-code', methods=['POST'])
def generate_qr_code():
    try:
        data = request.json or {}
        first_name = data.get('firstName', 'John')
        last_name = data.get('lastName', 'Doe')
        flight = data.get('flight', 'AI 202')
        from_airport = data.get('from', 'BOM')
        to_airport = data.get('to', 'DEL')
        date = data.get('date', '2024-09-15')
        time = data.get('time', '14:30')
        seat = data.get('seat', '15B')
        gate = data.get('gate', 'C12')
        pnr = data.get('pnr', 'XYZ789')

        qr_data = f"BOARDING PASS\nPassenger: {first_name} {last_name}\nFlight: {flight}\nFrom: {from_airport}\nTo: {to_airport}\nDate: {date}\nTime: {time}\nSeat: {seat}\nGate: {gate}\nPNR: {pnr}"

        qr_img = qrcode.make(qr_data)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"qr_code_{timestamp}_{unique_id}.png"
        filepath = os.path.join(IMAGES_FOLDER, filename)
        
        qr_img.save(filepath)
        image_url = f"{BASE_URL}/images/{filename}"

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
        flight = data.get('flight', 'AI 202')
        from_airport = data.get('from', 'BOM')
        to_airport = data.get('to', 'DEL')
        date = data.get('date', '2024-09-15')
        time = data.get('time', '14:30')
        seat = data.get('seat', '15B')
        gate = data.get('gate', 'C12')
        pnr = data.get('pnr', 'XYZ789')

        barcode_data = pnr
        
        barcode_class = barcode.get_barcode_class('code128')
        barcode_img = barcode_class(barcode_data, writer=ImageWriter())
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"barcode_{timestamp}_{unique_id}.png"
        filepath = os.path.join(IMAGES_FOLDER, filename)
        
        barcode_img.save(filepath)
        image_url = f"{BASE_URL}/images/{filename}"

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

@app.route('/images/<filename>')
def serve_image(filename):
    try:
        return app.send_static_file(filename)
    except:
        return jsonify({'error': 'Image not found'}), 404

if __name__ == '__main__':
    app.static_folder = IMAGES_FOLDER
    app.static_url_path = '/images'
    
    print("Starting Boarding Pass Generator...")
    print("Server: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
