# ClawMeter

Free OpenClaw cost tracking dashboard. Track your token usage, predict costs, and stay within budget.

## Features

- Real-time token usage tracking
- Cost estimation by model
- Budget alerts
- Simple, clean dashboard

## Quick Start

```bash
# Clone the repo
git clone https://github.com/Euronymousx/clawmeter.git
cd clawmeter

# Install dependencies
pip install -r requirements.txt

# Run
python app.py
```

## Configuration

Set your OpenClaw API endpoint in `config.py`:

```python
OPENCLAW_API_URL = "http://localhost:3000/api"
```

## License

MIT
