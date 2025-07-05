#!/usr/bin/env python3
"""
Basic setup verification script for summer-vibe-hackathon
Run this to verify all dependencies are installed correctly
"""

import sys
import os
from dotenv import load_dotenv

def test_nodejs_setup():
    """Test if Node.js dependencies are installed"""
    print("\n📦 Testing Node.js setup...")
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Check if package.json exists
    package_json_path = os.path.join(project_root, 'package.json')
    if not os.path.exists(package_json_path):
        print("❌ package.json not found")
        return False
    
    print("✅ package.json found")
    
    # Check if node_modules exists (indicates npm install was run)
    node_modules_path = os.path.join(project_root, 'node_modules')
    if os.path.exists(node_modules_path):
        print("✅ node_modules directory exists (npm install was run)")
        
        # Check for some key packages
        key_packages = ['express', 'firebase', 'dotenv']
        for package in key_packages:
            package_path = os.path.join(node_modules_path, package)
            if os.path.exists(package_path):
                print(f"✅ {package} package installed")
            else:
                print(f"⚠️  {package} package not found")
        
        return True
    else:
        print("❌ node_modules directory not found")
        print("📝 Run: npm install")
        return False

def test_python_imports():
    """Test if all required Python packages can be imported"""
    print("🐍 Testing Python imports...")
    
    packages = [
        ('requests', 'HTTP requests library'),
        ('langchain', 'LangChain AI framework'),
        ('firebase_admin', 'Firebase Admin SDK'),
        ('dotenv', 'Environment variable loader'),
        ('pandas', 'Data processing library'),
        ('pytest', 'Testing framework')
    ]
    
    failed_imports = []
    
    for package, description in packages:
        try:
            __import__(package)
            print(f"✅ {package} imported successfully ({description})")
        except ImportError as e:
            print(f"❌ Failed to import {package}: {e}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\n📝 Missing packages. Install with:")
        print(f"   pip install {' '.join(failed_imports)}")
        print(f"   or run: pip install -r requirements.txt")
    
    return len(failed_imports) == 0

def test_environment_variables():
    """Test if environment variables are loaded"""
    print("\n🔑 Testing environment variables...")
    
    load_dotenv()
    
    required_vars = [
        ('TAVILY_API_KEY', 'Tavily search API'),
        ('OPENAI_API_KEY', 'OpenAI/LangChain API'),
        ('FIREBASE_PROJECT_ID', 'Firebase project')
    ]
    
    optional_vars = [
        ('SUPERWHISPER_API_KEY', 'Superwhisper voice API'),
        ('DEBUG', 'Development mode'),
        ('PORT', 'Server port')
    ]
    
    missing_vars = []
    
    for var, description in required_vars:
        value = os.getenv(var)
        if value and value != f'your_{var.lower()}_here' and 'your_' not in value.lower():
            print(f"✅ {var} is set ({description})")
        else:
            print(f"❌ {var} is not set or has placeholder value ({description})")
            missing_vars.append(var)
    
    for var, description in optional_vars:
        value = os.getenv(var)
        if value and 'your_' not in value.lower():
            print(f"✅ {var} is set ({description})")
        else:
            print(f"⚠️  {var} is not set ({description}) - optional")
    
    if missing_vars:
        print(f"\n📝 Please set these required environment variables in your .env file:")
        for var in missing_vars:
            print(f"   - {var}")
    
    return len(missing_vars) == 0

def test_directory_structure():
    """Test if all required directories exist"""
    print("📁 Testing directory structure...")
    
    required_dirs = [
        ('src/api', 'Tavily API integration'),
        ('src/agent', 'LangChain agent logic'),
        ('src/ui', 'Windsurf UI components'),
        ('src/voice', 'Superwhisper integration'),
        ('src/storage', 'Firebase storage'),
        ('src/tests', 'Test files'),
        ('data', 'JSON data files'),
        ('docs', 'Documentation and media'),
        ('setup', 'Setup and verification scripts')
    ]
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    missing_dirs = []
    
    for dir_path, description in required_dirs:
        full_path = os.path.join(project_root, dir_path)
        if os.path.exists(full_path):
            print(f"✅ {dir_path} exists ({description})")
        else:
            print(f"❌ {dir_path} is missing ({description})")
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"\n📝 Create missing directories with:")
        for dir_path in missing_dirs:
            print(f"   mkdir -p {dir_path}")
    
    return len(missing_dirs) == 0

def test_config_files():
    """Test if required configuration files exist"""
    print("\n📄 Testing configuration files...")
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    config_files = [
        ('requirements.txt', 'Python dependencies'),
        ('package.json', 'Node.js dependencies'),
        ('.env', 'Environment variables'),
        ('.gitignore', 'Git ignore rules')
    ]
    
    missing_files = []
    
    for file_name, description in config_files:
        file_path = os.path.join(project_root, file_name)
        if os.path.exists(file_path):
            print(f"✅ {file_name} exists ({description})")
        else:
            print(f"❌ {file_name} is missing ({description})")
            missing_files.append(file_name)
    
    return len(missing_files) == 0

def run_quick_api_test():
    """Quick test to verify API connectivity (if keys are set)"""
    print("\n🌐 Testing API connectivity...")
    
    load_dotenv()
    
    # Test if we can at least import and initialize (without making actual calls)
    tavily_key = os.getenv('TAVILY_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    if tavily_key and 'your_' not in tavily_key.lower():
        try:
            import requests
            # Don't make actual API call, just verify we have the tools
            print("✅ Tavily API key set and requests library available")
        except ImportError:
            print("❌ Tavily API key set but requests library not available")
            return False
    else:
        print("⚠️  Tavily API key not set - skipping connectivity test")
    
    if openai_key and 'your_' not in openai_key.lower():
        try:
            import langchain
            print("✅ OpenAI API key set and LangChain available")
        except ImportError:
            print("❌ OpenAI API key set but LangChain not available")
            return False
    else:
        print("⚠️  OpenAI API key not set - skipping connectivity test")
    
    return True

if __name__ == "__main__":
    print("🚀 Summer Vibe Hackathon - Setup Verification")
    print("=" * 50)
    
    tests = [
        ("Directory Structure", test_directory_structure),
        ("Configuration Files", test_config_files),
        ("Python Imports", test_python_imports),
        ("Node.js Setup", test_nodejs_setup),
        ("Environment Variables", test_environment_variables),
        ("API Connectivity", run_quick_api_test)
    ]
    
    tests_passed = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            tests_passed += 1
        print("-" * 30)
    
    print(f"\n📊 Final Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 Setup verification complete! Ready to start development.")
        print("\n🚀 Next steps:")
        print("   1. Start working on Issue #2 (Tavily API integration)")
        print("   2. Each team member should run this script after setup")
        print("   3. Share results on Discord")
        sys.exit(0)
    else:
        print("⚠️  Some issues found. Please resolve them before continuing.")
        print("\n🔧 Common fixes:")
        print("   - Run: pip install -r requirements.txt")
        print("   - Fill in real API keys in .env file")
        print("   - Create missing directories")
        print("   - Check Discord for team troubleshooting")
        sys.exit(1)
