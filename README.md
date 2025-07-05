# AirReserve

## Setup Instructions

### Prerequisites
1. Python 3.8+
2. Git
3. API Keys (see `.env.example`)

### Installation
1. Clone the repository:
```bash
git clone https://github.com/anshk8/AirReserve.git
cd AirReserve
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
- Copy `.env.example` to `.env`
- Fill in your API keys:
  - Tavily API Key
  - OpenAI API Key
  - Firebase credentials

4. Verify installation:
```bash
python src/test_setup.py
```

### Project Structure
```
AirReserve/
├── config/         # Configuration files
├── data/           # Data storage
├── docs/           # Documentation
├── src/
│   ├── api/       # API endpoints
│   ├── ui/        # User interface
│   └── tests/     # Test files
├── tests/          # Additional test files
└── setup/          # Setup scripts
```

### Development
1. Run the test script to verify setup:
```bash
python src/test_setup.py
```

2. Start the development server:
```bash
uvicorn src.main:app --reload
```

### Troubleshooting
- Ensure all API keys are correctly set in `.env`
- Check that Python dependencies are installed
- Verify Firebase credentials are properly configured

### Security
- Never commit `.env` file to version control
- Keep API keys secure
- Follow best practices for credential management

**Notification Config Updates:**  
If you see a new version or changes in `config/notification_config.template.json`, update your own `notification_config.json` to match, and re-add your webhook and any personal settings. The `config_version` field helps you track if your config is up to date.