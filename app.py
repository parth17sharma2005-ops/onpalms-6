from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv
from chat import SalesBotRAG
import json
import re
import requests
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS to allow requests from anywhere (production and testing)
CORS(app, 
     origins=['*'],  # Allow all origins
     allow_headers=['Content-Type', 'Authorization', 'X-Session-Id', 'Accept'],
     methods=['GET', 'POST', 'OPTIONS'],
     supports_credentials=True)

# Initialize the chatbot
chatbot = SalesBotRAG()

# Session storage (in production, use Redis or database)
sessions = {}

# Google Sheets integration - Updated with TOFU enhancement support
GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbwtkTDW3CjoKgSJrDgj2dWn6oU-ZXYncoGuu6h7zeB5lT14xe_8Q-yjtlwYxHZ61H77/exec'

def submit_to_google_sheets(name, email, phone, session_data=None):
    """Submit demo request to Google Sheets with enhanced TOFU data"""
    try:
        # Enhanced TOFU data capture
        lead_score = session_data.get('lead_score', 0) if session_data else 0
        stage = session_data.get('stage', 'unknown') if session_data else 'unknown'
        signals = ', '.join(session_data.get('qualification_signals', [])) if session_data else ''
        touch_count = session_data.get('touch_count', 0) if session_data else 0
        
        payload = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'name': name,
            'email': email,
            'phone': phone,
            'source': 'Localhost Demo Form',
            'lead_score': lead_score,
            'stage': stage,
            'qualification_signals': signals,
            'touch_count': touch_count,
            'conversation_length': len(session_data.get('conversation_history', [])) if session_data else 0
        }
        
        response = requests.post(GOOGLE_SCRIPT_URL, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Google Sheets: {result.get('message', 'Success')}")
            return True
        else:
            print(f"❌ Google Sheets error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Google Sheets submission failed: {str(e)}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        # Get or create session
        if session_id not in sessions:
            sessions[session_id] = {
                'conversation_history': [],
                'user_info': {},
                'lead_score': 0,
                'stage': 'greeting'
            }
        
        session = sessions[session_id]
        
        # Add user message to history
        session['conversation_history'].append({
            'role': 'user',
            'content': message
        })
        
        # Get bot response
        response = chatbot.get_response(message, session)
        
        # Add bot response to history
        session['conversation_history'].append({
            'role': 'assistant',
            'content': response['message']
        })
        
        # Update session
        sessions[session_id] = session
        
        return jsonify({
            'message': response['message'],
            'show_demo_form': response.get('show_demo_form', False),
            'lead_score': session.get('lead_score', 0),
            'stage': session.get('stage', 'greeting')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/submit_info', methods=['POST'])
def submit_info():
    """Handle info submission from inline forms (footer.php compatibility)"""
    try:
        data = request.json
        name = data.get('name', '')
        email = data.get('email', '')
        
        # Validate business email
        is_business = chatbot.validate_business_email(email)
        
        if not is_business:
            return jsonify({
                'success': False,
                'message': "Please provide a business email address. Personal email domains like Gmail, Yahoo, and Hotmail are not accepted.",
                'show_form_again': True
            })
        
        # Basic validation
        if not name or not email:
            return jsonify({
                'success': False,
                'message': "Please provide both name and email address.",
                'show_form_again': True
            })
        
        # Log the info submission
        print(f"Info submitted: {name} ({email})")
        
        return jsonify({
            'success': True,
            'message': f"Thank you {name}! Your information has been recorded. How can I assist you further?"
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f"An error occurred: {str(e)}",
            'show_form_again': False
        }), 500

@app.route('/submit_demo', methods=['POST'])
def submit_demo():
    try:
        data = request.json
        session_id = data.get('session_id', 'default')
        name = data.get('name', '')
        email = data.get('email', '')
        phone = data.get('phone', '')  # New optional field
        
        # Validate business email
        is_business = chatbot.validate_business_email(email)
        
        if not is_business:
            return jsonify({
                'success': False,
                'message': "Please provide a business email address. Personal email domains like Gmail, Yahoo, and Hotmail are not accepted for demo requests."
            })
        
        # Store lead information
        if session_id in sessions:
            sessions[session_id]['user_info'].update({
                'name': name,
                'email': email,
                'phone': phone,
                'demo_requested': True
            })
            sessions[session_id]['lead_score'] += 30
            sessions[session_id]['stage'] = 'demo_scheduled'
        
        # Submit to Google Sheets with enhanced TOFU data
        session_data = sessions.get(session_id, {})
        sheets_success = submit_to_google_sheets(name, email, phone, session_data)
        
        # Log the demo request
        print(f"Demo request: {name} ({email}), Phone: {phone}")
        if sheets_success:
            print("✅ Successfully saved to Google Sheets")
        else:
            print("⚠️ Google Sheets submission failed, but demo request recorded locally")
        
        return jsonify({
            'success': True,
            'message': f"Thank you {name}! Your demo request has been submitted. Our sales team will contact you at {email} within 24 hours to schedule your personalized PALMS™ demonstration.",
            'sheets_saved': sheets_success
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Use environment port for production deployment (Render, Heroku, etc.)
    port = int(os.environ.get('PORT', 5002))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=port)