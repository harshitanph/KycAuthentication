from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import pandas as pd
import datetime
import os
from PIL import Image
import io

app = FastAPI(title="AI-Powered KYC Verification API")

# ================================
# LOAD DATA (GNN Results)
# ================================
DATA_FILE = "output_of_GNN_part2-1.csv"
df = pd.read_csv(DATA_FILE)

LOG_FILE = "kyc_audit_log.csv"
if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=[
        "Timestamp", "Name", "ID_Type", "Document_Number",
        "Fraud_Risk_Level", "Fraud_Probability", "Confidence"
    ]).to_csv(LOG_FILE, index=False)


# ================================
# Helper: classify fraud risk
# ================================
def classify_risk(prob):
    if prob < 0.33:
        return "Low"
    elif prob < 0.67:
        return "Medium"
    else:
        return "High"


# ================================
# POST Endpoint: Verify KYC
# ================================
@app.post("/api/verify-kyc")
async def verify_kyc(
    id_image: UploadFile = File(..., description="Upload ID document image (Aadhaar, PAN, etc.)"),
    selfie_image: UploadFile = File(..., description="Upload selfie image for facial verification"),
    name: str = Form(..., description="User full name"),
    id_type: str = Form(..., description="Type of ID (Aadhaar, PAN, etc.)"),
    document_number: str = Form(..., description="Document number for verification")
):
    # Step 1: Read uploaded files
    try:
        id_img = Image.open(io.BytesIO(await id_image.read()))
        selfie_img = Image.open(io.BytesIO(await selfie_image.read()))
    except Exception:
        return JSONResponse(content={"status": "Error", "message": "Invalid image format"}, status_code=400)

    # Step 2: Look up document in dataset (mock check)
    record = df[df["Document_Number"].astype(str) == str(document_number)]
    if record.empty:
        return {"status": "Not Found", "message": "Document not found in database"}

    prob = float(record.iloc[0]["GNN_Fraud_Probability"])
    risk = classify_risk(prob)
    confidence = round((1 - prob) * 100, 2)  # Confidence % = 1 - fraud probability

    # Step 3: Log the verification
    log_entry = pd.DataFrame([{
        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Name": name,
        "ID_Type": id_type,
        "Document_Number": document_number,
        "Fraud_Risk_Level": risk,
        "Fraud_Probability": round(prob * 100, 2),
        "Confidence": confidence
    }])
    log_entry.to_csv(LOG_FILE, mode="a", header=False, index=False)

    # Step 4: Return response to frontend
    return {
        "status": "Verified" if risk != "High" else "Not Verified",
        "name": name,
        "id_type": id_type,
        "fraud_risk_level": risk,
        "fraud_probability": f"{round(prob * 100, 2)}%",
        "confidence": f"{confidence}%",
        "message": "Face and ID matched successfully" if risk != "High" else "Possible mismatch or anomaly detected"
    }


# ================================
# Root route
# ================================
@app.get("/")
def home():
    return {"message": "✅ KYC Verification API running. Use POST /api/verify-kyc for uploads."}
