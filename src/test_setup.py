import os
from dotenv import load_dotenv
from tavily import Tavily
from langchain.llms import OpenAI
from firebase_admin import initialize_app, credentials

# Load environment variables
load_dotenv()

def test_setup():
    print("\nTesting AirReserve Setup...\n")
    
    # Test Tavily API
    try:
        tavily = Tavily(api_key=os.getenv('TAVILY_API_KEY'))
        print("✅ Tavily API: Connected successfully")
    except Exception as e:
        print(f"❌ Tavily API: Error - {str(e)}")
    
    # Test OpenAI/LangChain
    try:
        llm = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        print("✅ OpenAI/LangChain: Connected successfully")
    except Exception as e:
        print(f"❌ OpenAI/LangChain: Error - {str(e)}")
    
    # Test Firebase
    try:
        cred = credentials.Certificate({
            "type": "service_account",
            "project_id": os.getenv('FIREBASE_PROJECT_ID'),
            "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
            "private_key": os.getenv('FIREBASE_PRIVATE_KEY'),
            "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
            "client_id": os.getenv('FIREBASE_CLIENT_ID'),
            "auth_uri": os.getenv('FIREBASE_AUTH_URI'),
            "token_uri": os.getenv('FIREBASE_TOKEN_URI')
        })
        initialize_app(cred)
        print("✅ Firebase: Connected successfully")
    except Exception as e:
        print(f"❌ Firebase: Error - {str(e)}")
    
    print("\nSetup verification complete!")

if __name__ == "__main__":
    test_setup()
