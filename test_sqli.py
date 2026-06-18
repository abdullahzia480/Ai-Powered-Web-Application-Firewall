import requests

url = "http://localhost:5000/login"
payload = {
    "username": "admin' OR 1=1 --",
    "password": "test"
}

print("Testing SQL Injection Attack on SentinAI WAF")
print("Attack payload:", payload["username"])
print("-" * 60)

try:
    response = requests.post(url, data=payload)
    print("Status Code:", response.status_code)
    
    # Check if blocked
    if response.status_code == 403:
        print("✅ SUCCESS: Attack BLOCKED with 403 Forbidden!")
    elif "blocked" in response.text.lower():
        print("✅ SUCCESS: Attack BLOCKED by WAF!")
    elif "sentin" in response.text.lower() and response.status_code == 200:
        print("✅ SUCCESS: Redirected to blocked page!")
    else:
        print("❌ FAILED: Attack went through")
        print("First 200 chars of response:", response.text[:200])
        
except Exception as e:
    print("Error:", str(e))
