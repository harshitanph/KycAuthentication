🚀 KYC Verification Backend

A complete backend system for AI-powered KYC (Know Your Customer) Verification built using FastAPI.
It processes user details, runs them through an ML pipeline, predicts fraud probability, and returns a structured verification result.

🎯 What This Backend Does

This backend implements a full KYC verification workflow:

Receives data from the frontend (name, document number, address, document type)

Loads trained ML models (best_model, scaler, feature_selector)

Extracts & processes features (selection → scaling → prediction)

Predicts fraud probability and risk levels

Returns structured JSON response (fraud probability, risk, confidence, etc.)

Logs all verification activity into an audit CSV

📋 Complete Flow

Frontend Request → Backend Processing → Response → Frontend Display

1️⃣ Frontend Request
POST /api/verify-kyc
{
  "name": "John Doe",
  "documentNumber": "123456789012",
  "address": "123 Main St",
  "documentType": "AADHAR"
}

2️⃣ Backend Processing

Extract features

Apply feature selection

Scale features

Run ML model

Compute fraud probability

Assign risk level

Log entry

3️⃣ Response
{
  "status": "Verified",
  "fraudProbability": 25.5,
  "riskLevel": "Low",
  "confidence": 74.5
}

🚀 Quick Start
Install Dependencies
cd backend
pip install -r requirements.txt

Run Server
uvicorn main:app --reload --host 0.0.0.0 --port 8000


API will run at:
➡️ http://localhost:8000

Test With CURL
curl -X POST "http://localhost:8000/api/verify-kyc" \
-H "Content-Type: application/json" \
-d '{ "name": "Test User", "documentNumber": "123456789012", "address": "Test Address", "documentType": "AADHAR" }'

📁 File Structure
backend/
├── main.py                    # Main FastAPI application
├── requirements.txt           # Python dependencies
├── best_model (1).pkl         # Trained ML model
├── scaler (1).pkl             # Feature scaler
├── feature_selector (1).pkl   # Feature selector
├── output_of_GNN_part2-1.csv  # GNN results (fallback)
├── kyc_audit_log.csv          # Audit log (auto-created)
├── BACKEND_ANALYSIS.md        # Analysis document
├── IMPLEMENTATION_GUIDE.md    # Detailed guide
└── README.md                  # This file

🔌 API Endpoints
✅ POST /api/verify-kyc

Purpose: Run KYC verification & fraud prediction.

Request Body
{
  "name": "John Doe",
  "documentNumber": "123456789012",
  "address": "123 Main St, City",
  "documentType": "AADHAR"
}

Response
{
  "status": "Verified",
  "id": "VER1703123456789",
  "timestamp": "2025-01-15T10:30:00",
  "name": "John Doe",
  "documentNumber": "123456789012",
  "fraudProbability": 15.5,
  "riskLevel": "Low",
  "confidence": 84.5,
  "details": {
    "documentAuthenticity": "Valid",
    "addressVerification": "Verified",
    "anomalyScore": "15.50"
  },
  "message": "Face & ID match successful"
}

✅ GET /

Health check & model load status

Response
{
  "message": "✅ KYC Verification API running",
  "status": "operational",
  "models": {
    "main_model": "✅ Loaded",
    "scaler": "✅ Loaded",
    "feature_selector": "✅ Loaded"
  }
}

✅ GET /api/history

Fetches verification history from audit log.

🧠 How It Works
🔹 Model Loading

Models load once at startup

If missing, backend continues with fallback

Alerts shown in logs

🔹 Feature Engineering

Features extracted automatically such as:

Text lengths

Word counts

Document type encoding

Uppercase/digit counts

Validation flags

🔹 Prediction Pipeline

Extract features

Feature selection (optional)

Scale features

Model prediction

Convert probability → risk level

<33% = Low

33–67% = Medium

>67% = High

🔹 Error Handling

Missing models → fallback

Invalid data → HTTP 400

Prediction errors → safe response + logged

🔧 Configuration
Model Files (Place in backend/)

best_model (1).pkl

scaler (1).pkl

feature_selector (1).pkl

Change Port
uvicorn main:app --port 8080

📊 Logging

Logs include:

Model load status

Prediction requests

Errors & warnings

Full audit trail (kyc_audit_log.csv)

🔗 Frontend Integration
Example Fetch Call
const response = await fetch('http://localhost:8000/api/verify-kyc', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: formData.name,
    documentNumber: formData.aadharNumber,
    address: formData.address,
    documentType: formData.documentType
  })
});

const result = await response.json();

⚠️ Important Notes

Modify extract_features() if model input format changes

Ensure pickle versions match installed scikit-learn

CORS currently allows all origins (*) — restrict later

Backend still works without model files (but less accurate)

🐛 Troubleshooting
✔ Models not loading?

Check file names & paths

Ensure compatible Python version

✔ Wrong predictions?

Verify feature engineering

Check training vs inference features

✔ Port issues?
netstat -ano | findstr :8000
uvicorn main:app --port 8001

📝 Next Steps

Improve feature engineering

Add image (ID/selfie) verification

Replace CSV logs with database

Add authentication (API keys/JWT)

Add rate limiting

📚 Documentation

BACKEND_ANALYSIS.md – Explanation of workflow

IMPLEMENTATION_GUIDE.md – Step-by-step implementation

README.md – This file

🎉 Ready to Use!

Start your server and connect your frontend — your full KYC system is operational.
