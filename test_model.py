import joblib
import os

# Load the model
model_path = os.path.join('waftool', 'firewall_model.pkl')
print(f"Loading model from: {model_path}")
model = joblib.load(model_path)

print("Model loaded successfully!")
print(f"Model type: {type(model)}")

# Test with SQL injection
test_payloads = [
    "admin' OR 1=1 --",
    "admin",
    "' OR '1'='1",
    "hello world"
]

print("\nTesting predictions:")
for payload in test_payloads:
    prediction = model.predict([payload])[0]
    proba = model.predict_proba([payload])[0]
    print(f"  '{payload}' => Prediction: {prediction} | Malicious Prob: {proba[1]:.3f}")
