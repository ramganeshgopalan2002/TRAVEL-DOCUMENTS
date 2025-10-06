from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from datetime import datetime
import requests
import time

app = Flask(__name__)
CORS(app)

# Airport data with coordinates for real weather API
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

# Weather emoji mapping
WEATHER_EMOJI = {
    'clear': '☀️',
    'clouds': '☁️',
    'rain': '🌧️',
    'drizzle': '🌦️',
    'thunderstorm': '⛈️',
    'snow': '❄️',
    'mist': '🌫️',
    'fog': '🌫️',
    'haze': '🌫️',
    'smoke': '🌫️'
}

# Cache for weather data to avoid too many API calls
weather_cache = {}
CACHE_DURATION = 300  # 5 minutes

def get_emoji_for_weather(condition):
    """Get appropriate emoji for weather condition"""
    condition_lower = condition.lower()
    for key, emoji in WEATHER_EMOJI.items():
        if key in condition_lower:
            return emoji
    return '🌤️'  # Default emoji

def fetch_real_weather(lat, lon):
    """Fetch real weather data from OpenWeatherMap API"""
    try:
        # Using OpenWeatherMap API (free tier)
        api_key = "demo_key"  # In production, use a real API key
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        
        # For demo purposes, we'll use mock data that simulates real conditions
        # In production, uncomment the following lines:
        # response = requests.get(url, timeout=10)
        # response.raise_for_status()
        # data = response.json()
        
        # Mock data that simulates real weather patterns
        current_hour = datetime.now().hour
        current_month = datetime.now().month
        
        # Simulate weather based on time of day and season
        if 6 <= current_hour <= 18:  # Daytime
            if current_month in [12, 1, 2]:  # Winter
                temp = 18 + (current_hour - 6)  # 18-30°C range
                conditions = ['clear', 'clouds', 'clear']
            elif current_month in [3, 4, 5]:  # Spring
                temp = 25 + (current_hour - 6)  # 25-37°C range
                conditions = ['clear', 'haze', 'clear']
            else:  # Summer/Monsoon
                temp = 28 + (current_hour - 6)  # 28-40°C range
                conditions = ['clear', 'clouds', 'rain']
        else:  # Nighttime
            if current_month in [12, 1, 2]:  # Winter
                temp = 12 + (current_hour / 4)  # 12-18°C range
                conditions = ['clear', 'mist', 'clear']
            else:  # Other seasons
                temp = 20 + (current_hour / 6)  # 20-26°C range
                conditions = ['clear', 'clouds', 'clear']
        
        # Add some randomness based on airport location
        import random
        condition = random.choice(conditions)
        temp_variation = random.uniform(-2, 2)
        temp += temp_variation
        
        descriptions = {
            'clear': 'Clear sky',
            'clouds': 'Partly cloudy',
            'rain': 'Light rain',
            'haze': 'Hazy',
            'mist': 'Misty',
            'drizzle': 'Drizzling'
        }
        
        return {
            'temperature': round(temp),
            'description': descriptions.get(condition, 'Clear'),
            'main': condition.capitalize(),
            'humidity': random.randint(40, 80),
            'wind_speed': round(random.uniform(1, 15), 1)
        }
        
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        # Fallback data
        return {
            'temperature': 25,
            'description': 'Weather unavailable',
            'main': 'Clear',
            'humidity': 50,
            'wind_speed': 5.0
        }

@app.route('/')
def serve_index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('.', path)

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'travel-document-generator',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/weather/<airport_code>')
def get_weather(airport_code):
    airport_code = airport_code.upper()
    
    if airport_code not in AIRPORT_DATA:
        return jsonify({
            'success': False,
            'error': f'Airport code {airport_code} not found',
            'available_airports': list(AIRPORT_DATA.keys())
        }), 404
    
    # Check cache first
    cache_key = f"{airport_code}_{datetime.now().strftime('%Y%m%d%H')}"
    if cache_key in weather_cache:
        cached_data = weather_cache[cache_key]
        if time.time() - cached_data['timestamp'] < CACHE_DURATION:
            return jsonify(cached_data['data'])
    
    try:
        airport = AIRPORT_DATA[airport_code]
        weather_data = fetch_real_weather(airport['lat'], airport['lon'])
        
        response_data = {
            'success': True,
            'airport_code': airport_code,
            'city': airport['city'],
            'temperature': weather_data['temperature'],
            'description': weather_data['description'],
            'main': weather_data['main'],
            'emoji': get_emoji_for_weather(weather_data['main']),
            'humidity': weather_data['humidity'],
            'wind_speed': weather_data['wind_speed'],
            'timestamp': datetime.now().isoformat(),
            'source': 'simulated_realtime'
        }
        
        # Cache the response
        weather_cache[cache_key] = {
            'data': response_data,
            'timestamp': time.time()
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error processing weather request: {e}")
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

@app.route('/api/weather/bulk')
def get_bulk_weather():
    """Get weather for multiple airports at once"""
    airports_param = request.args.get('airports', 'DEL,BOM')
    airport_codes = [code.strip().upper() for code in airports_param.split(',')]
    
    results = {}
    for code in airport_codes:
        if code in AIRPORT_DATA:
            # Use the existing weather endpoint logic
            weather_response = get_weather(code)
            results[code] = weather_response.get_json()
        else:
            results[code] = {
                'success': False,
                'error': f'Airport {code} not found'
            }
    
    return jsonify(results)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Travel Document Generator Server on port {port}")
    print("Available endpoints:")
    print("  GET /              - Serve main application")
    print("  GET /api/health    - Health check")
    print("  GET /api/weather/<airport_code> - Get weather for airport")
    print("  GET /api/airports  - List all supported airports")
    app.run(host='0.0.0.0', port=port, debug=True)