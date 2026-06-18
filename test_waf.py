import requests

# Test the WAF with SQL injection
url = "http://localhost:5000/login"

print("Testing SentinAI WAF...")
print("=" * 60)

# Test 1: Normal login (should pass)
print("\n1. Testing normal login:")
try:
    response = requests.post(url, data={"username": "admin", "password": "password123"})
    print(f"   Status Code: {response.status_code}")
    if "blocked" in response.text.lower() or "sentin" in response.text.lower():
        print("   Result: BLOCKED by WAF")
    else:
        print("   Result: ALLOWED")
except Exception as e:
    print(f"   Error: {e}")

# Test 2: SQL Injection (should be blocked)
print("\n2. Testing SQL injection attack:")
try:
    response = requests.post(url, data={"username": "admin' OR 1=1 --", "password": "test"})
    print(f"   Status Code: {response.status_code}")
    if "blocked" in response.text.lower() or "sentin" in response.text.lower():
        print("   Result: ✅ BLOCKED by WAF (SUCCESS!)")
    elif response.status_code == 403:
        print("   Result: ✅ BLOCKED with 403 Forbidden (SUCCESS!)")
    else:
        print("   Result: ❌ ATTACK WENT THROUGH (FAILED)")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 60)
