from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime

app = Flask(__name__)

# In-memory storage for demo (replace with database in production)
users = {}

# Model pricing
MODEL_PRICING = {
    'kimi-k2': {'name': 'Kimi K2.5', 'input': 0.001, 'output': 0.001},
    'gpt-4o': {'name': 'GPT-4o', 'input': 0.005, 'output': 0.015},
    'gpt-4o-mini': {'name': 'GPT-4o Mini', 'input': 0.00015, 'output': 0.0006},
    'claude-3-5-sonnet': {'name': 'Claude 3.5 Sonnet', 'input': 0.003, 'output': 0.015},
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/demo-data')
def demo_data():
    """Return demo usage data for the dashboard"""
    return jsonify({
        'connected': True,
        'instance_name': 'Demo OpenClaw',
        'today': {
            'requests': 47,
            'input_tokens': 125000,
            'output_tokens': 89000,
            'cost': 0.214
        },
        'this_week': {
            'requests': 312,
            'input_tokens': 892000,
            'output_tokens': 654000,
            'cost': 1.546
        },
        'this_month': {
            'requests': 1254,
            'input_tokens': 3429000,
            'output_tokens': 2100000,
            'cost': 5.529
        },
        'models_used': {
            'kimi-k2': {'requests': 892, 'cost': 3.784},
            'gpt-4o': {'requests': 362, 'cost': 1.745}
        },
        'budget': 20.00,
        'budget_remaining': 14.47
    })

@app.route('/api/pricing')
def pricing():
    return jsonify(MODEL_PRICING)

@app.route('/api/waitlist', methods=['POST'])
def waitlist():
    email = request.json.get('email')
    # In production, save to database
    print(f"New waitlist signup: {email}")
    return jsonify({'success': True, 'message': 'Thanks! We\'ll notify you when access is available.'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
