# Setup Directory

This directory contains setup and verification tools for the Summer Vibe Hackathon project.

## Files in this directory:

### `test_setup.py` - Setup Verification Script
**Purpose:** Verifies that your development environment is properly configured

**What it checks:**
- ✅ Directory structure matches project requirements
- ✅ All configuration files exist (requirements.txt, package.json, .env, .gitignore)
- ✅ Python packages are installed correctly
- ✅ Environment variables are set with real API keys
- ✅ Basic API connectivity preparation

## How to Use

### For everyone:
1. Clone the repository
2. Install dependencies:
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt

   # Install Node.js dependencies
   npm install
   ```
3. Copy and fill in your API keys:
   ```bash
   # Copy the .env file and add your real API keys
   cp .env .env.local
   # Edit .env with your actual API keys
   ```
4. Run the verification script:
   ```bash
   python setup/test_setup.py
   ```

## Expected Output

### ✅ Successful Setup:`
```
🚀 Summer Vibe Hackathon - Setup Verification
==================================================

Directory Structure:
✅ src/api exists (Tavily API integration)
✅ src/agent exists (LangChain agent logic)
✅ src/ui exists (Windsurf UI components)
...

📊 Final Results: 5/5 tests passed
🎉 Setup verification complete! Ready to start development.
```

### ❌ Issues Found:
```
🚀 Summer Vibe Hackathon - Setup Verification
==================================================

Python Imports:
❌ Failed to import langchain: No module named 'langchain'

Environment Variables:
❌ TAVILY_API_KEY is not set or has placeholder value

📊 Final Results: 3/5 tests passed
⚠️  Some issues found. Please resolve them before continuing.
```

## Troubleshooting

### macOS: pyaudio installation fails
**Error:** `fatal error: 'portaudio.h' file not found`
**Solution:**
```bash
brew install portaudio
pip install -r requirements.txt
```

### Windows: pyaudio installation fails
**Solution:**
```bash
# Use pre-compiled wheel
pip install pipwin
pipwin install pyaudio
```

### Linux: pyaudio installation fails
**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install portaudio19-dev

# CentOS/RHEL
sudo yum install portaudio-devel
```

### Common Issues:

#### 1. **Missing Python Packages**
```bash
# Install all Python packages
pip install -r requirements.txt
```

#### 2. **Missing Node.js Packages**
```bash
# Install all JavaScript packages
npm install
```

#### 3. **API Keys Not Set**
- Edit your `.env` file
- Replace placeholder values with real API keys
- Make sure there are no extra spaces or quotes

#### 3. **Missing Directories**
```bash
# Create any missing directories
mkdir -p src/api src/agent src/ui src/voice src/storage src/tests data docs
```

#### 4. **Import Errors**
- Make sure you're in the correct directory (project root)
- Activate your virtual environment if using one
- Check Python version (recommended: Python 3.8+)

### Getting API Keys:

#### Tavily API:
1. Go to [Tavily AI](https://tavily.com)
2. Sign up for an account
3. Get your API key from the dashboard

#### OpenAI API:
1. Go to [OpenAI Platform](https://platform.openai.com)
2. Create an account
3. Generate an API key in the API section

#### Firebase:
1. Go to [Firebase Console](https://console.firebase.google.com)
2. Create a new project
3. Go to Project Settings → Service Accounts
4. Generate a new private key

#### Notes
1. Re-run this test script if you encounter environment issues later

---

*This setup ensures all team members have identical, working development environments for the hackathon.*
