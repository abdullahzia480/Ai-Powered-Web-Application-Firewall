from website.app import create_app
from waftool.middleware import SentinAIFirewall

# 1. Initialize the Vulnerable Website
app = create_app()

# 2. Attach the SentinAI Security Tool
# This wraps the app and injects the WAF logic
print(">>> ACTIVATING SENTIN_AI PROTECTION SYSTEM (UPDATED) <<<")
firewall = SentinAIFirewall(app)

if __name__ == "__main__":
    # Run the protected application
    app.run(host='0.0.0.0', port=5000, debug=True)
