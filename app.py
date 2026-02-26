from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)

DATA_FILE = '/app/data/usage.json'

# Ensure data directory exists
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

# Model pricing (per 1K tokens)
MODEL_PRICING = {
    'kimi-k2': {'input': 0.001, 'output': 0.001, 'name': 'Kimi K2.5'},
    'gpt-4o': {'input': 0.005, 'output': 0.015, 'name': 'GPT-4o'},
    'gpt-4o-mini': {'input': 0.00015, 'output': 0.0006, 'name': 'GPT-4o Mini'},
    'claude-3-5-sonnet': {'input': 0.003, 'output': 0.015, 'name': 'Claude 3.5 Sonnet'},
    'claude-3-opus': {'input': 0.015, 'output': 0.075, 'name': 'Claude 3 Opus'},
    'claude-3-haiku': {'input': 0.00025, 'output': 0.00125, 'name': 'Claude 3 Haiku'},
}

def load_data():
    """Load usage data from file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'entries': [], 'budget': 100.0}

def save_data(data):
    """Save usage data to file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def calculate_costs(data):
    """Calculate costs from entries"""
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    today_cost = 0
    week_cost = 0
    month_cost = 0
    total_tokens = 0
    
    for entry in data.get('entries', []):
        entry_date = datetime.fromisoformat(entry['date']).date()
        cost = entry['cost']
        
        if entry_date == today:
            today_cost += cost
        if entry_date >= week_ago:
            week_cost += cost
        if entry_date >= month_ago:
            month_cost += cost
        
        total_tokens += entry.get('input_tokens', 0) + entry.get('output_tokens', 0)
    
    return {
        'today': round(today_cost, 4),
        'this_week': round(week_cost, 4),
        'this_month': round(month_cost, 4),
        'total_tokens': total_tokens,
        'budget': data.get('budget', 100.0),
        'remaining': round(data.get('budget', 100.0) - month_cost, 4)
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get current status"""
    data = load_data()
    costs = calculate_costs(data)
    
    return jsonify({
        'connected': True,
        'message': 'ClawMeter Active - Manual Entry Mode',
        'data': {
            'session_tokens': costs['total_tokens'],
            'estimated_cost': costs['this_month'],
            'model': 'Multi-Model',
            'uptime': 'Active'
        }
    })

@app.route('/api/costs')
def get_costs():
    """Get cost breakdown"""
    data = load_data()
    costs = calculate_costs(data)
    
    return jsonify({
        'models': {k: {'name': v['name'], 'input': v['input'], 'output': v['output']} 
                   for k, v in MODEL_PRICING.items()},
        'today': {
            'tokens': 0,
            'cost': costs['today']
        },
        'this_week': {
            'tokens': 0,
            'cost': costs['this_week']
        },
        'this_month': {
            'tokens': costs['total_tokens'],
            'cost': costs['this_month']
        },
        'budget': costs['budget'],
        'remaining': costs['remaining']
    })

@app.route('/api/entries', methods=['GET', 'POST'])
def entries():
    """Get or add usage entries"""
    data = load_data()
    
    if request.method == 'POST':
        entry = request.json
        entry['date'] = datetime.now().isoformat()
        entry['id'] = len(data['entries']) + 1
        
        # Calculate cost
        model = entry.get('model', 'kimi-k2')
        input_tokens = entry.get('input_tokens', 0)
        output_tokens = entry.get('output_tokens', 0)
        
        if model in MODEL_PRICING:
            pricing = MODEL_PRICING[model]
            cost = (input_tokens / 1000 * pricing['input']) + (output_tokens / 1000 * pricing['output'])
            entry['cost'] = round(cost, 6)
        else:
            entry['cost'] = 0
        
        data['entries'].append(entry)
        save_data(data)
        
        return jsonify({'success': True, 'entry': entry})
    
    # GET - return recent entries
    return jsonify({
        'entries': data['entries'][-50:][::-1]  # Last 50, newest first
    })

@app.route('/api/budget', methods=['POST'])
def set_budget():
    """Set monthly budget"""
    data = load_data()
    data['budget'] = request.json.get('budget', 100.0)
    save_data(data)
    return jsonify({'success': True, 'budget': data['budget']})

@app.route('/api/entry/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    """Delete an entry"""
    data = load_data()
    data['entries'] = [e for e in data['entries'] if e['id'] != entry_id]
    save_data(data)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
