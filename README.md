# 🛡️ SentinAI: AI-Powered Web Application Firewall

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgrey.svg)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-Machine%20Learning-orange.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

## Overview

SentinAI is an AI-powered Web Application Firewall (WAF) developed to detect and mitigate malicious web requests using machine learning techniques. Unlike traditional rule-based firewalls that rely solely on predefined signatures, SentinAI employs a trained machine learning model to analyze incoming HTTP requests and identify potentially malicious behavior such as SQL Injection attacks.

The project demonstrates the integration of Machine Learning with modern web security practices and provides a practical framework for intelligent request filtering, threat monitoring, and real-time alerting.

---

## Key Features

### AI-Based Threat Detection

* Machine Learning powered request classification
* TF-IDF feature extraction
* Logistic Regression classification model
* Real-time request evaluation

### Web Application Protection

* SQL Injection detection and blocking
* Suspicious payload identification
* Request interception through middleware
* Configurable risk assessment

### Monitoring and Analytics

* Real-time dashboard
* Traffic statistics and visualizations
* Attack logging and event tracking
* Historical request analysis

### Instant Notifications

* Telegram alert integration
* Attack notifications for administrators
* Real-time incident reporting

### Portable Architecture

* Modular Flask middleware design
* Easy integration into existing Flask applications
* Reusable security component

---

## System Architecture

```text
Client Request
      │
      ▼
SentinAI Middleware
      │
      ▼
AI Detection Engine
(TF-IDF + Logistic Regression)
      │
 ┌────┴────┐
 │         │
 ▼         ▼
Allow    Block
 │         │
 ▼         ▼
Application  Alert + Log
```

---

## Project Structure

```text
SentinAI/
│
├── run_system.py
├── requirements.txt
├── PROJECT_DOCUMENTATION.txt
│
├── waftool/
│   ├── ai_engine.py
│   ├── middleware.py
│   ├── alerts.py
│   ├── firewall_model.pkl
│   ├── templates/
│   └── static/
│
├── website/
│   ├── app.py
│   ├── templates/
│   └── static/
│
├── tests/
│   ├── test_model.py
│   ├── test_waf.py
│   ├── test_sqli.py
│   └── test_telegram.py
│
└── datasets/
```

---

## Core Components

### AI Engine (`ai_engine.py`)

Responsible for:

* Loading the trained machine learning model
* Extracting request features
* Performing threat classification
* Returning risk predictions

### Middleware (`middleware.py`)

Responsible for:

* Intercepting HTTP requests
* Processing request payloads
* Invoking the AI engine
* Allowing or blocking traffic

### Alert System (`alerts.py`)

Responsible for:

* Telegram integration
* Incident notifications
* Security event reporting

### Dashboard

Provides:

* Real-time monitoring
* Attack visualization
* Security analytics
* Traffic insights

---

## Machine Learning Pipeline

1. Request data is collected from incoming HTTP traffic.
2. Relevant payloads are extracted and normalized.
3. TF-IDF vectorization converts text into numerical features.
4. Logistic Regression evaluates the request.
5. The system assigns a risk score.
6. Suspicious requests are blocked and logged.
7. Alerts are generated for administrators.

---

## Installation

### Prerequisites

* Python 3.11+
* pip
* Git

### Clone Repository

```bash
git clone https://github.com/abdullahzia480/Ai-Powered-Web-Application-Firewall.git
cd Ai-Powered-Web-Application-Firewall
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Telegram Alerts (Optional)

Edit:

```text
waftool/alerts.py
```

Add your:

* Telegram Bot Token
* Chat ID

---

## Running the Project

Start the system:

```bash
python run_system.py
```

Default URLs:

| Component       | URL                                 |
| --------------- | ----------------------------------- |
| Web Application | http://localhost:5000               |
| Login Portal    | http://localhost:5000/login         |
| WAF Dashboard   | http://localhost:5000/waf/dashboard |

---

## Demonstration

To test SQL Injection detection:

Navigate to:

```text
http://localhost:5000/login
```

Example payload:

```sql
admin' OR 1=1 --
```

Expected behavior:

* Request intercepted
* Threat classified
* Request blocked
* Dashboard updated
* Telegram alert generated (if configured)

---

## Integrating SentinAI Into Your Own Flask Project

Copy the `waftool` directory into your application.

Example:

```python
from flask import Flask
from waftool import SentinAIFirewall

app = Flask(__name__)

firewall = SentinAIFirewall(app)

if __name__ == "__main__":
    app.run()
```

---

## Technologies Used

* Python
* Flask
* Scikit-Learn
* Logistic Regression
* TF-IDF Vectorization
* Chart.js
* HTML/CSS/JavaScript
* Telegram Bot API

---

## Future Enhancements

* XSS detection support
* CSRF attack detection
* Deep learning-based classification
* Adaptive learning mechanisms
* Cloud deployment support
* SIEM integration
* Threat intelligence feeds

---

## Research Significance

This project explores the practical application of Machine Learning within Web Application Firewalls and demonstrates how AI-assisted security mechanisms can complement traditional rule-based approaches for web application protection.

---

## Disclaimer

This project was developed for educational, research, and demonstration purposes. It is not intended for direct production deployment without additional security testing, validation, and auditing.
