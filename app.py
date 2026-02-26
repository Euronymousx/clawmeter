from flask import Flask, render_template, jsonify, request
import requests
import os

app = Flask(__name__)

# Configuration - update this to your OpenClaw instance
OPENCLAW_API_URL = os.environ.get('OPENCLAW_API_URL', 'http://localhost:3000/api')

# Model pricing (per 1K tokens)
MODEL_PRICING = {
    'gpt-4': {'input': 0.03, 'output': 0.06},
    'gpt-4-turbo': {'input': 0.01, 'output': 0.03},
    'gpt-3.5-turbo': {'input': 0.0005, 'output': 0.0015},
    'claude-3-opus': {'input': 0.015, 'output': 0.075},
    'claude-3-sonnet': {'input': 0.003, 'output': 0.015},
    'claude-3-haiku': {'input': 0.00025, 'output': 0.00125},
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get current OpenClaw status"""
    try:
        # Try to fetch from OpenClaw API
        response = requests.get(f"{OPENCLAW_API_URL}/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return jsonify({
                'connected': True,
                'data': data
            })
    except:
        pass
    
    # Fallback: return mock data for demo
    return jsonify({
        'connected': False,
        'message': 'OpenClaw not connected. Showing demo data.',
        'demo_data': {
            'session_tokens': 15420,
            'estimated_cost': 0.47,
            'model': 'gpt-3.5-turbo',
            'uptime': '2h 34m'
        }
    })

@app.route('/api/costs')
def get_costs():
    """Get cost breakdown"""
    return jsonify({
        'models': MODEL_PRICING,
        'today': {
            'tokens': 15420,
            'cost': 0.47
        },
        'this_week': {
            'tokens': 89234,
            'cost': 2.89
        },
        'this_month': {
            'tokens': 342891,
            'cost': 12.45
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
