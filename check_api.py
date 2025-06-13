import requests
import json

def check_api_status():
    """Check if the FastAPI is running and accessible"""
    
    # Test different URLs
    test_urls = [
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]
    
    print("🔍 Checking API status...\n")
    
    for base_url in test_urls:
        print(f"Testing: {base_url}")
        
        # Test health endpoint
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            print(f"✅ Health endpoint: Status {response.status_code}")
            print(f"📋 Response: {response.json()}")
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to {base_url}")
        except requests.exceptions.Timeout:
            print(f"⏰ Timeout connecting to {base_url}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 50)
    
    # Test if port 8000 is in use
    print("\n🔍 Checking if port 8000 is in use...")
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 8000))
    sock.close()
    
    if result == 0:
        print("✅ Port 8000 is open and something is listening")
    else:
        print("❌ Port 8000 is not accessible")
        print("💡 Make sure you started the API with: uvicorn app_fastapi:app --host 0.0.0.0 --port 8000")

if __name__ == "__main__":
    check_api_status()
