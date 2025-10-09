from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv
from chat import SalesBotRAG
import json
import re

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize the chatbot
chatbot = SalesBotRAG()

# Session storage (in production, use Redis or database)
sessions = {}

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

@app.route('/submit_demo', methods=['POST'])
def submit_demo():
    try:
        data = request.json
        session_id = data.get('session_id', 'default')
        name = data.get('name', '')
        email = data.get('email', '')
        
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
                'demo_requested': True
            })
            sessions[session_id]['lead_score'] += 30
            sessions[session_id]['stage'] = 'demo_scheduled'
        
        # In a real application, you would save this to your CRM
        print(f"Demo request: {name} ({email})")
        
        return jsonify({
            'success': True,
            'message': f"Thank you {name}! Your demo request has been submitted. Our sales team will contact you at {email} within 24 hours to schedule your personalized PALMS™ demonstration."
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)