KYC Verification Backend
🎯 What This Backend Does
This backend implements a complete KYC (Know Your Customer) verification system that:

Receives data from frontend (name, document number, address, document type)
Loads trained ML models (best_model, scaler, feature_selector)
Processes data through ML pipeline (feature extraction → selection → scaling → prediction)
Returns fraud prediction (Fraud or Not, with probability scores and risk levels)
📋 Complete Flow
Frontend Request
    ↓
POST /api/verify-kyc
{
  "name": "John Doe",
  "documentNumber": "123456789012",
  "address": "123 Main St",
  "documentType": "AADHAR"
}
    ↓
Backend Processing
    ↓
1. Extract Features from input data
2. Apply Feature Selection (if model available)
3. Scale Features (if scaler available)
4. Run ML Model Prediction
5. Calculate Risk Level (Low/Medium/High)
6. Log to Audit File
    ↓
Response
{
  "status": "Verified" | "Flagged",
  "fraudProbability": 25.5,
  "riskLevel": "Low",
  "confidence": 74.5,
  ...
}
    ↓
Frontend Displays Results
🚀 Quick Start
1. Install Dependencies
cd backend
pip install -r requirements.txt
2. Run Server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
The API will be available at: http://localhost:8000

3. Test It
Visit http://localhost:8000 in browser to see API status.

Or use curl:

curl -X POST "http://localhost:8000/api/verify-kyc" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "documentNumber": "123456789012",
    "address": "Test Address",
    "documentType": "AADHAR"
  }'
📁 File Structure
backend/
├── main.py                    # Main FastAPI application
├── requirements.txt          # Python dependencies
├── best_model (1).pkl        # Trained ML model
├── scaler (1).pkl            # Feature scaler
├── feature_selector (1).pkl  # Feature selector
├── output_of_GNN_part2-1.csv # GNN results (fallback)
├── kyc_audit_log.csv         # Audit log (auto-created)
├── BACKEND_ANALYSIS.md       # Analysis document
├── IMPLEMENTATION_GUIDE.md   # Detailed guide
└── README.md                 # This file
🔌 API Endpoints
POST /api/verify-kyc (Main Endpoint)
Purpose: Verify KYC data and get fraud prediction

Request Body (JSON):

{
  "name": "John Doe",
  "documentNumber": "123456789012",
  "address": "123 Main St, City",
  "documentType": "AADHAR"
}
Response:

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
GET /
Purpose: Health check and model status

Response:

{
  "message": "✅ KYC Verification API running",
  "status": "operational",
  "models": {
    "main_model": "✅ Loaded",
    "scaler": "✅ Loaded",
    "feature_selector": "✅ Loaded"
  }
}
GET /api/history
Purpose: Get verification history

Response: Array of verification records from audit log

🧠 How It Works
Model Loading
Models are loaded once at server startup
If a model file is missing, the system logs a warning but continues
Falls back to GNN CSV data if models unavailable
Feature Engineering
The backend extracts features from input data:

Text lengths (name, document number, address)
Document validation flags
Document type encoding (AADHAR=0, PAN=1, UTILITY=2)
Address word count
Name analysis (uppercase, digits)
Prediction Pipeline
Extract features from input
Apply feature selection (if available)
Scale features (if scaler available)
Run model prediction
Convert probability to risk level:
< 33%: Low risk
33-67%: Medium risk
67%: High risk

Error Handling
Missing models: Falls back to GNN CSV or safe defaults
Invalid input: Returns HTTP 400 with error message
Prediction errors: Logs error and returns safe values
All operations are logged
🔧 Configuration
Model Files
Place your trained models in the backend/ directory:

best_model (1).pkl - Main prediction model
scaler (1).pkl - Feature scaler
feature_selector (1).pkl - Feature selector (optional)
Port Configuration
Default port: 8000 Change in main.py or use uvicorn command:

uvicorn main:app --port 8080
📊 Logging
All operations are logged:

Model loading status
Prediction requests
Errors and warnings
Audit trail in kyc_audit_log.csv
🔗 Frontend Integration
The frontend should call the API like this:

const response = await fetch('http://localhost:8000/api/verify-kyc', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: formData.name,
    documentNumber: formData.aadharNumber,
    address: formData.address,
    documentType: formData.documentType
  })
});

const result = await response.json();
// result contains: status, fraudProbability, riskLevel, etc.
⚠️ Important Notes
Feature Engineering: The extract_features() function may need adjustment based on how your model was trained. If your model expects different features, modify this function.

Model Compatibility: Ensure your pickle files are compatible with the scikit-learn version installed.

CORS: Currently allows all origins (*). For production, restrict to your frontend domain.

Model Files: The backend will work even if some model files are missing, but predictions will be less accurate.

🐛 Troubleshooting
Models not loading?
Check file paths in main.py
Ensure pickle files are in backend/ directory
Check Python version compatibility
Predictions seem wrong?
Verify feature extraction matches training data format
Check model file compatibility
Review logs for errors
Port already in use?
# Find process using port 8000
netstat -ano | findstr :8000
# Kill process or use different port
uvicorn main:app --port 8001
📝 Next Steps
Customize Feature Engineering: Adjust extract_features() to match your training data
Add Image Processing: If you need to process ID/selfie images, add computer vision logic
Database Integration: Replace CSV logging with database
Authentication: Add API keys or JWT tokens for security
Rate Limiting: Add rate limiting to prevent abuse
📚 Documentation
BACKEND_ANALYSIS.md - Analysis of what was needed
IMPLEMENTATION_GUIDE.md - Detailed technical guide
README.md - This file
Ready to use! Start the server and connect your frontend. 🚀
