from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import qrcode
import barcode
from barcode.writer import ImageWriter
import os
from datetime import datetime
import uuid
import random

app = Flask(__name__)
CORS(app)

# Use a relative path for the images folder
IMAGES_FOLDER = 'static/images'
BASE_URL = '/'  # Use relative base URL

# Ensure the images folder exists
os.makedirs(os.path.join(app.root_path, IMAGES_FOLDER), exist_ok=True)

# Airport data
AIRPORT_DATA = {
    'DEL': {'city': 'Delhi', 'lat': 28.6139, 'lon': 77.2090},
    'BOM': {'city': 'Mumbai', 'lat': 19.0760, 'lon': 72.8777},
    'BLR': {'city': 'Bangalore', 'lat': 12.9716, 'lon': 77.5946},
    'MAA': {'city': 'Chennai', 'lat': 13.0827, 'lon': 80.2707},
    'HYD': {'city': 'Hyderabad', 'lat': 17.3850, 'lon': 78.4867},
    'CCU': {'city': 'Kolkata', 'lat': 22.5726, 'lon': 88.3639},
    'AMD': {'city': 'Ahmedabad', 'lat': 23.0225, 'lon': 72.5714},
    'GOI': {'city': 'Goa', 'lat': 15.2993, 'lon': 74.1240},
    'PNQ': {'city': 'Pune', 'lat': 18.5204, 'lon': 73.8567},
    'COK': {'city': 'Kochi', 'lat': 9.9312, 'lon': 76.2673}
}

# Weather configurations for different cities
WEATHER_CONFIGS = {
    'DEL': {'base_temp': 25, 'variation': 10, 'conditions': ['Clear', 'Haze', 'Cloudy']},
    'BOM': {'base_temp': 28, 'variation': 5, 'conditions': ['Humid', 'Cloudy', 'Light Rain']},
    'BLR': {'base_temp': 26, 'variation': 4, 'conditions': ['Mild', 'Cloudy', 'Clear']},
    'MAA': {'base_temp': 30, 'variation': 3, 'conditions': ['Hot', 'Humid', 'Clear']},
    'HYD': {'base_temp': 29, 'variation': 4, 'conditions': ['Clear', 'Hot', 'Cloudy']},
    'CCU': {'base_temp': 27, 'variation': 5, 'conditions': ['Humid', 'Cloudy', 'Rain']},
    'AMD': {'base_temp': 32, 'variation': 6, 'conditions': ['Hot', 'Clear', 'Dry']},
    'GOI': {'base_temp': 27, 'variation': 3, 'conditions': ['Pleasant', 'Breezy', 'Clear']},
    'PNQ': {'base_temp': 26, 'variation': 4, 'conditions': ['Mild', 'Clear', 'Cloudy']},
    'COK': {'base_temp': 28, 'variation': 3, 'conditions': ['Humid', 'Rain', 'Cloudy']}
}

# Weather emoji mapping
WEATHER_EMOJI = {
    'Clear': '☀️',
    'Cloudy': '☁️',
    'Rain': '🌧️',
    'Light Rain': '🌦️',
    'Thunderstorm': '⛈️',
    'Snow': '❄️',
    'Mist': '🌫️',
    'Fog': '🌫️',
    'Haze': '🌫️',
    'Humid': '💧',
    'Hot': '🔥',
    'Mild': '🌤️',
    'Pleasant': '😊',
    'Breezy': '💨',
    'Dry': '🏜️'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'success': True,
        'message': 'Travel Document Generator API is running',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/generate/qr-code', methods=['POST'])
def generate_qr_code():
    try:
        data = request.json or {}
        
        # Extract data based on current mode
        if 'etFirstName' in data:  # E-Ticket mode
            first_name = data.get('etFirstName', 'Rahul')
            last_name = data.get('etLastName', 'Sharma')
            flight = data.get('etFlight', 'AI 2727')
            from_airport = data.get('etFrom', 'BOM')
            to_airport = data.get('etTo', 'DEL')
            date = data.get('etDate', '2025-09-10')
            time = data.get('etTime', '13:15')
            pnr = data.get('pnrEt', 'ABC123')
            ticket_number = data.get('ticketNumber', '1234567890123')
            
            qr_data = f"E-TICKET\nTicket: {ticket_number}\nPassenger: {first_name} {last_name}\nFlight: {flight}\nFrom: {from_airport}\nTo: {to_airport}\nDate: {date}\nTime: {time}\nPNR: {pnr}"
        
        elif 'bagFirstName' in data:  # Baggage Tag mode
            first_name = data.get('bagFirstName', 'Priya')
            last_name = data.get('bagLastName', 'Patel')
            flight = data.get('bagFlight', 'AI0121')
            from_airport = data.get('bagFrom', 'BOM')
            to_airport = data.get('bagTo', 'DEL')
            pnr = data.get('bagPnr', 'ABC123')
            bag_number = data.get('bagNumber', '0000-615742')
            
            qr_data = f"BAGGAGE TAG\nPassenger: {first_name} {last_name}\nFlight: {flight}\nFrom: {from_airport}\nTo: {to_airport}\nPNR: {pnr}\nTag: {bag_number}"
        
        else:  # Boarding Pass mode (default)
            first_name = data.get('firstName', 'Rahul')
            last_name = data.get('lastName', 'Sharma')
            flight = data.get('flight', 'AI 2727')
            from_airport = data.get('from', 'BOM')
            to_airport = data.get('to', 'DEL')
            date = data.get('date', '2025-09-10')
            time = data.get('time', '13:15')
            seat = data.get('seat', '17A')
            gate = data.get('gate', '07')
            pnr = data.get('pnr', 'ABC123')
            boarding_time = data.get('boardingTime', '12:45')
            flight_class = data.get('class', 'Y')
            sequence = data.get('sequence', '001A')
            
            qr_data = f"BOARDING PASS\nPassenger: {first_name} {last_name}\nFlight: {flight}\nFrom: {from_airport}\nTo: {to_airport}\nDate: {date}\nTime: {time}\nSeat: {seat}\nGate: {gate}\nPNR: {pnr}\nBoarding: {boarding_time}\nClass: {flight_class}\nSeq: {sequence}"

        # Generate QR code
        qr_img = qrcode.make(qr_data)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"qr_code_{timestamp}_{unique_id}.png"
        
        # Construct the full file path
        filepath = os.path.join(app.root_path, IMAGES_FOLDER, filename)
        
        # Save QR code to file
        qr_img.save(filepath)
        
        # Generate the URL for the image
        image_url = f"/static/images/{filename}"

        return jsonify({
            'success': True,
            'data': {
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
        
        # Determine barcode content based on mode
        if 'bagNumber' in data:  # Baggage Tag mode
            barcode_data = data.get('bagNumber', '0000-615742')
        elif 'ticketNumber' in data:  # E-Ticket mode
            barcode_data = data.get('ticketNumber', '1234567890123')
        else:  # Boarding Pass mode (default)
            barcode_data = data.get('pnr', 'ABC123')

        # Generate barcode (using Code128 format)
        barcode_class = barcode.get_barcode_class('code128')
        barcode_img = barcode_class(barcode_data, writer=ImageWriter())
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"barcode_{timestamp}_{unique_id}.png"
        
        # Construct the full file path
        filepath = os.path.join(app.root_path, IMAGES_FOLDER, filename)
        
        # Save barcode to file
        barcode_img.save(filepath)
        
        # Generate the URL for the image
        image_url = f"/static/images/{filename}"

        return jsonify({
            'success': True,
            'data': {
                'barcodeImageUrl': image_url,
                'filename': filename,
                'barcodeData': barcode_data
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/weather/<airport_code>')
def get_weather(airport_code):
    airport_code = airport_code.upper()
    
    if airport_code not in AIRPORT_DATA:
        return jsonify({
            'success': False,
            'error': f'Airport code {airport_code} not found',
            'available_airports': list(AIRPORT_DATA.keys())
        }), 404
    
    try:
        # Get weather config for this airport
        config = WEATHER_CONFIGS.get(airport_code, WEATHER_CONFIGS['DEL'])
        
        # Generate realistic temperature based on time of day
        current_hour = datetime.now().hour
        time_factor = abs(12 - current_hour) / 12  # 0 at noon, 1 at midnight
        temp_variation = random.uniform(-config['variation'], config['variation'])
        
        # Base temperature is cooler at night, warmer during day
        if 6 <= current_hour <= 18:  # Daytime
            base_temp = config['base_temp'] + 2
        else:  # Nighttime
            base_temp = config['base_temp'] - 2
            
        temperature = round(base_temp + temp_variation)
        
        # Select weather condition
        condition = random.choice(config['conditions'])
        emoji = WEATHER_EMOJI.get(condition, '🌤️')
        
        response_data = {
            'success': True,
            'airport_code': airport_code,
            'city': AIRPORT_DATA[airport_code]['city'],
            'temperature': temperature,
            'description': condition,
            'main': condition,
            'emoji': emoji,
            'humidity': random.randint(40, 85),
            'wind_speed': round(random.uniform(1, 15), 1),
            'timestamp': datetime.now().isoformat(),
            'source': 'simulated_realtime'
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Unable to fetch weather data',
            'airport_code': airport_code,
            'city': AIRPORT_DATA.get(airport_code, {}).get('city', 'Unknown')
        }), 500

@app.route('/api/airports')
def list_airports():
    airports_list = []
    for code, info in AIRPORT_DATA.items():
        airports_list.append({
            'code': code,
            'city': info['city'],
            'coordinates': {
                'lat': info['lat'],
                'lon': info['lon']
            }
        })
    
    return jsonify({
        'success': True,
        'airports': airports_list,
        'count': len(airports_list)
    })

# Route to serve images with CORS headers
@app.route('/static/images/<filename>')
def serve_image(filename):
    response = send_from_directory(os.path.join(app.root_path, IMAGES_FOLDER), filename)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Route to serve static files
@app.route('/<path:filename>')
def serve_static(filename):
    response = send_from_directory('.', filename)
    if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
        response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting Travel Document Generator Server on port {port}")
    print("📍 Available endpoints:")
    print("   GET /                     - Serve main application")
    print("   GET /api/health           - Health check")
    print("   POST /api/generate/qr-code - Generate QR code")
    print("   POST /api/generate/barcode - Generate barcode")
    print("   GET /api/weather/<code>   - Get weather for airport")
    print("   GET /api/airports         - List all supported airports")
    print("")
    print("📋 Supported airport codes:", list(AIRPORT_DATA.keys()))
    print("")
    print("🌐 Server will be available at: http://localhost:5000")
    
    app.run(host='0.0.0.0', port=port, debug=True)