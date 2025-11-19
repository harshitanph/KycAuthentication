# # from fastapi import FastAPI, HTTPException, UploadFile, File
# # from fastapi.responses import JSONResponse
# # from fastapi.middleware.cors import CORSMiddleware
# # from pydantic import BaseModel
# # import pandas as pd
# # import datetime
# # import os
# # import joblib
# # import numpy as np
# # from typing import Optional, List
# # import logging
# # from pathlib import Path
# # import io

# # # ======================================
# # # LOGGING
# # # ======================================
# # logging.basicConfig(level=logging.INFO)
# # logger = logging.getLogger("main")

# # # ======================================
# # # FASTAPI SETUP
# # # ======================================
# # app = FastAPI(title="AI-Powered KYC Verification API")

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # ======================================
# # # PATHS
# # # ======================================
# # BASE_DIR = Path(__file__).parent
# # MODEL_PATH = BASE_DIR / "best_model.pkl"
# # SCALER_PATH = BASE_DIR / "scaler.pkl"
# # FEATURE_SELECTOR_PATH = BASE_DIR / "feature_selector.pkl"
# # GNN_CSV = BASE_DIR / "output_of_GNN_part2.csv"
# # AUDIT_LOG = BASE_DIR / "kyc_audit_log.csv"

# # # ======================================
# # # GLOBALS
# # # ======================================
# # model = None
# # scaler = None
# # feature_selector = None
# # gnn_df = pd.DataFrame()

# # # ======================================
# # # REQUEST MODELS
# # # ======================================
# # class VerificationRequest(BaseModel):
# #     name: str
# #     documentNumber: str
# #     address: Optional[str] = ""
# #     documentType: str  # PASSPORT / AADHAR / PAN

# # class VerificationResponse(BaseModel):
# #     status: str
# #     id: str
# #     timestamp: str
# #     name: str
# #     documentNumber: str
# #     fraudProbability: float
# #     riskLevel: str
# #     confidence: float
# #     details: dict
# #     message: str

# # class BatchResultItem(BaseModel):
# #     row: int
# #     name: str
# #     documentNumber: str
# #     address: str
# #     documentType: str
# #     status: str
# #     id: str
# #     timestamp: str
# #     fraudProbability: float
# #     riskLevel: str
# #     confidence: float
# #     details: dict
# #     message: str
# #     error: Optional[str] = None

# # class BatchVerificationResponse(BaseModel):
# #     total: int
# #     successful: int
# #     failed: int
# #     results: List[BatchResultItem]

# # # ======================================
# # # CREATE GNN CSV IF MISSING
# # # ======================================
# # def ensure_gnn_csv():
# #     if not GNN_CSV.exists():
# #         logger.warning("⚠️ Creating new GNN CSV file because it was missing.")
# #         df = pd.DataFrame({
# #             "Document_Number": [],
# #             "GNN_Fraud_Probability": []
# #         })
# #         df.to_csv(GNN_CSV, index=False)
# #         logger.info(f"✅ Created empty GNN CSV at {GNN_CSV}")

# # # ======================================
# # # LOAD MODELS
# # # ======================================
# # def load_models():
# #     global model, scaler, feature_selector
# #     try:
# #         model = joblib.load(MODEL_PATH)
# #         logger.info("✅ Loaded ML model")
# #     except Exception as e:
# #         logger.error(f"❌ Model load failed: {e}")
# #         model = None

# #     try:
# #         scaler = joblib.load(SCALER_PATH)
# #         logger.info("✅ Loaded scaler")
# #     except Exception as e:
# #         logger.error(f"❌ Scaler load failed: {e}")
# #         scaler = None

# #     try:
# #         feature_selector = joblib.load(FEATURE_SELECTOR_PATH)
# #         logger.info("✅ Loaded feature selector")
# #     except Exception as e:
# #         logger.error(f"❌ Feature selector load failed: {e}")
# #         feature_selector = None

# # # ======================================
# # # LOAD GNN OUTPUT CSV
# # # ======================================
# # def load_gnn():
# #     global gnn_df
# #     try:
# #         if not GNN_CSV.exists():
# #             logger.warning("⚠️ GNN CSV not found. Creating new...")
# #             ensure_gnn_csv()
# #         df = pd.read_csv(GNN_CSV)
# #         if df.empty:
# #             logger.warning("⚠️ GNN CSV is empty.")
# #             gnn_df = pd.DataFrame()
# #         else:
# #             gnn_df = df
# #             logger.info(f"✅ Loaded GNN CSV with {len(gnn_df)} rows")
# #     except Exception as e:
# #         logger.error(f"❌ Error loading GNN CSV: {e}")
# #         gnn_df = pd.DataFrame()

# # # ======================================
# # # FEATURE EXTRACTION
# # # ======================================
# # def extract_features(name, doc, address, dtype):
# #     features = [
# #         len(name),
# #         len(doc),
# #         len(address),
# #         1 if doc.isdigit() else 0,
# #         len(set(doc)),
# #         1 if dtype == "AADHAR" else 0,
# #         1 if dtype == "PAN" else 0,
# #         1 if dtype in ["PASSPORT", "UTILITY"] else 0,
# #         len(address.split()),
# #         len(name.split()),
# #         1 if any(x.isupper() for x in name) else 0,
# #         1 if any(x.isdigit() for x in name) else 0,
# #     ]
# #     return np.array(features).reshape(1, -1)

# # # ======================================
# # # RISK LABEL
# # # ======================================
# # def classify(prob):
# #     if prob < 0.33:
# #         return "Low"
# #     elif prob < 0.67:
# #         return "Medium"
# #     return "High"

# # # ======================================
# # # GNN FALLBACK
# # # ======================================
# # def gnn_pred(doc):
# #     try:
# #         if gnn_df.empty:
# #             return 0.50
# #         row = gnn_df[gnn_df["Document_Number"].astype(str) == str(doc)]
# #         if not row.empty:
# #             return float(row.iloc[0]["GNN_Fraud_Probability"])
# #     except:
# #         pass
# #     return 0.50

# # # ======================================
# # # FULL PREDICTION
# # # ======================================
# # def predict_fraud(name, doc, address, dtype):
# #     X = extract_features(name, doc, address, dtype)
# #     if feature_selector:
# #         try:
# #             X = feature_selector.transform(X)
# #         except Exception as e:
# #             logger.warning(f"Feature selector failed: {e}")
# #     if scaler:
# #         try:
# #             X = scaler.transform(X)
# #         except Exception as e:
# #             logger.warning(f"Scaler failed: {e}")
# #     if model:
# #         try:
# #             proba_result = model.predict_proba(X)
# #             if proba_result.shape[1] == 2:
# #                 prob = float(proba_result[0][1])
# #             elif proba_result.shape[1] == 1:
# #                 prob = float(proba_result[0][0])
# #             else:
# #                 prob = float(proba_result[0][-1])
# #         except Exception as e:
# #             logger.error(f"Model prediction failed: {e}, using GNN fallback")
# #             prob = gnn_pred(doc)
# #     else:
# #         prob = gnn_pred(doc)
# #     prob = max(0.0, min(1.0, prob))
# #     risk = classify(prob)
# #     return {
# #         "fraud_probability": prob * 100,
# #         "risk_level": risk,
# #         "confidence": (1 - prob) * 100,
# #         "status": "Flagged" if risk == "High" else "Verified"
# #     }

# # # ======================================
# # # APP STARTUP
# # # ======================================
# # @app.on_event("startup")
# # def startup_event():
# #     logger.info("🚀 Booting API...")
# #     ensure_gnn_csv()
# #     load_models()
# #     load_gnn()
# #     logger.info("✅ Ready!")

# # # ======================================
# # # MAIN API ENDPOINT
# # # ======================================
# # @app.post("/api/verify-kyc", response_model=VerificationResponse)
# # def verify(request: VerificationRequest):
# #     result = predict_fraud(request.name, request.documentNumber, request.address, request.documentType)
# #     vid = f"VER{int(datetime.datetime.now().timestamp() * 1000)}"
# #     ts = datetime.datetime.now().isoformat()
# #     try:
# #         df = pd.DataFrame([{
# #             "Timestamp": ts,
# #             "Name": request.name,
# #             "ID_Type": request.documentType,
# #             "Document_Number": request.documentNumber,
# #             "Fraud_Risk": result["risk_level"],
# #             "Fraud_Probability": result["fraud_probability"],
# #         }])
# #         df.to_csv(AUDIT_LOG, mode="a", header=not AUDIT_LOG.exists(), index=False)
# #     except Exception as e:
# #         logger.warning(f"⚠️ Could not write audit log: {e}")
# #     return VerificationResponse(
# #         status=result["status"],
# #         id=vid,
# #         timestamp=ts,
# #         name=request.name,
# #         documentNumber=request.documentNumber,
# #         fraudProbability=result["fraud_probability"],
# #         riskLevel=result["risk_level"],
# #         confidence=result["confidence"],
# #         details={
# #             "documentAuthenticity": "Valid",
# #             "addressVerification": "Verified" if request.address and len(request.address) > 10 else "Pending",
# #             "anomalyScore": f"{result['fraud_probability']:.2f}"
# #         },
# #         message="KYC processed successfully."
# #     )

# # # ======================================
# # # ROOT CHECK
# # # ======================================
# # @app.get("/")
# # def home():
# #     return {
# #         "message": "KYC API running",
# #         "model": "Loaded" if model else "Not Loaded",
# #         "scaler": "Loaded" if scaler else "Not Loaded",
# #         "selector": "Loaded" if feature_selector else "Not Loaded",
# #         "gnn_csv": "Available" if not gnn_df.empty else "Empty"
# #     }

# # # ======================================
# # # DEBUG TEST PREDICTION
# # # ======================================
# # @app.get("/admin/test-prediction")
# # def test_prediction():
# #     test_cases = [
# #         {"name": "John Doe", "doc": "123456789", "address": "123 Main St", "dtype": "PASSPORT"},
# #         {"name": "Jane Smith", "doc": "987654321", "address": "456 Oak Ave", "dtype": "AADHAR"},
# #     ]
# #     results = []
# #     for test in test_cases:
# #         X = extract_features(test["name"], test["doc"], test["address"], test["dtype"])
# #         result = {"input": test, "features_shape": X.shape, "features": X.tolist()[0]}
# #         if feature_selector:
# #             try:
# #                 X_sel = feature_selector.transform(X)
# #                 result["after_selector_shape"] = X_sel.shape
# #                 result["after_selector"] = X_sel.tolist()[0]
# #                 X = X_sel
# #             except Exception as e:
# #                 result["selector_error"] = str(e)
# #         if scaler:
# #             try:
# #                 X_scaled = scaler.transform(X)
# #                 result["after_scaler_shape"] = X_scaled.shape
# #                 result["after_scaler"] = X_scaled.tolist()[0]
# #                 X = X_scaled
# #             except Exception as e:
# #                 result["scaler_error"] = str(e)
# #         if model:
# #             try:
# #                 proba = model.predict_proba(X)
# #                 result["model_proba_shape"] = proba.shape
# #                 result["model_proba"] = proba.tolist()[0]
# #                 result["fraud_prob"] = float(proba[0][1])
# #                 result["prediction"] = predict_fraud(test["name"], test["doc"], test["address"], test["dtype"])
# #             except Exception as e:
# #                 result["model_error"] = str(e)
# #         results.append(result)
# #     return {"model_loaded": model is not None, "scaler_loaded": scaler is not None, "selector_loaded": feature_selector is not None, "test_results": results}


# from fastapi import FastAPI, HTTPException, UploadFile, File
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import pandas as pd
# import datetime
# import os
# import joblib
# import numpy as np
# from typing import Optional, List
# import logging
# from pathlib import Path
# import io

# # ======================================
# # LOGGING
# # ======================================
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger("main")

# # ======================================
# # FASTAPI SETUP
# # ======================================
# app = FastAPI(title="AI-Powered KYC Verification API")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ======================================
# # PATHS
# # ======================================
# BASE_DIR = Path(__file__).parent
# MODEL_PATH = BASE_DIR / "best_model.pkl"
# SCALER_PATH = BASE_DIR / "scaler.pkl"
# FEATURE_SELECTOR_PATH = BASE_DIR / "feature_selector.pkl"
# GNN_CSV = BASE_DIR / "output_of_GNN_part2.csv"
# AUDIT_LOG = BASE_DIR / "kyc_audit_log.csv"

# # ======================================
# # GLOBALS
# # ======================================
# model = None
# scaler = None
# feature_selector = None
# gnn_df = pd.DataFrame()

# # ======================================
# # REQUEST MODELS
# # ======================================
# class VerificationRequest(BaseModel):
#     name: str
#     documentNumber: str
#     address: Optional[str] = ""
#     documentType: str  # PASSPORT / AADHAR / PAN

# class VerificationResponse(BaseModel):
#     status: str
#     id: str
#     timestamp: str
#     name: str
#     documentNumber: str
#     fraudProbability: float
#     riskLevel: str
#     confidence: float
#     details: dict
#     message: str

# class BatchResultItem(BaseModel):
#     row: int
#     name: str
#     documentNumber: str
#     address: str
#     documentType: str
#     status: str
#     id: str
#     timestamp: str
#     fraudProbability: float
#     riskLevel: str
#     confidence: float
#     details: dict
#     message: str
#     error: Optional[str] = None

# class BatchVerificationResponse(BaseModel):
#     total: int
#     successful: int
#     failed: int
#     results: List[BatchResultItem]

# # ======================================
# # CREATE GNN CSV IF MISSING
# # ======================================
# def ensure_gnn_csv():
#     if not GNN_CSV.exists():
#         logger.warning("⚠️ Creating new GNN CSV file because it was missing.")
#         df = pd.DataFrame({
#             "Document_Number": [],
#             "GNN_Fraud_Probability": []
#         })
#         df.to_csv(GNN_CSV, index=False)
#         logger.info(f"✅ Created empty GNN CSV at {GNN_CSV}")

# # ======================================
# # LOAD MODELS
# # ======================================
# def load_models():
#     global model, scaler, feature_selector
#     try:
#         model = joblib.load(MODEL_PATH)
#         logger.info("✅ Loaded ML model")
#     except Exception as e:
#         logger.error(f"❌ Model load failed: {e}")
#         model = None

#     try:
#         scaler = joblib.load(SCALER_PATH)
#         logger.info("✅ Loaded scaler")
#     except Exception as e:
#         logger.error(f"❌ Scaler load failed: {e}")
#         scaler = None

#     try:
#         feature_selector = joblib.load(FEATURE_SELECTOR_PATH)
#         logger.info("✅ Loaded feature selector")
#     except Exception as e:
#         logger.error(f"❌ Feature selector load failed: {e}")
#         feature_selector = None

# # ======================================
# # LOAD GNN OUTPUT CSV
# # ======================================
# def load_gnn():
#     global gnn_df
#     try:
#         if not GNN_CSV.exists():
#             logger.warning("⚠️ GNN CSV not found. Creating new...")
#             ensure_gnn_csv()
#         df = pd.read_csv(GNN_CSV)
#         if df.empty:
#             logger.warning("⚠️ GNN CSV is empty.")
#             gnn_df = pd.DataFrame()
#         else:
#             gnn_df = df
#             logger.info(f"✅ Loaded GNN CSV with {len(gnn_df)} rows")
#     except Exception as e:
#         logger.error(f"❌ Error loading GNN CSV: {e}")
#         gnn_df = pd.DataFrame()

# # ======================================
# # FEATURE EXTRACTION - ENHANCED
# # ======================================
# def extract_features(name, doc, address, dtype):
#     """
#     Extract features with more variance to avoid constant predictions
#     """
#     # Basic features
#     name_len = len(name)
#     doc_len = len(doc)
#     address_len = len(address)
    
#     # Document validation
#     doc_is_numeric = 1 if doc.isdigit() else 0
#     doc_unique_chars = len(set(doc))
    
#     # Document type encoding
#     is_aadhar = 1 if dtype == "AADHAR" else 0
#     is_pan = 1 if dtype == "PAN" else 0
#     is_other = 1 if dtype in ["PASSPORT", "UTILITY"] else 0
    
#     # Address analysis
#     address_words = len(address.split())
    
#     # Name analysis
#     name_words = len(name.split())
#     name_has_upper = 1 if any(x.isupper() for x in name) else 0
#     name_has_digit = 1 if any(x.isdigit() for x in name) else 0
    
#     # NEW: Additional variance features
#     # Check for suspicious patterns
#     has_repeated_chars = 1 if doc and len(set(doc)) < len(doc) * 0.5 else 0
#     name_all_caps = 1 if name.isupper() else 0
#     address_has_numbers = 1 if any(c.isdigit() for c in address) else 0
    
#     features = [
#         name_len,
#         doc_len,
#         address_len,
#         doc_is_numeric,
#         doc_unique_chars,
#         is_aadhar,
#         is_pan,
#         is_other,
#         address_words,
#         name_words,
#         name_has_upper,
#         name_has_digit,
#         has_repeated_chars,
#         name_all_caps,
#         address_has_numbers,
#     ]
    
#     return np.array(features).reshape(1, -1)

# # ======================================
# # RISK LABEL
# # ======================================
# def classify(prob):
#     if prob < 0.33:
#         return "Low"
#     elif prob < 0.67:
#         return "Medium"
#     return "High"

# # ======================================
# # DOCUMENT VALIDATION
# # ======================================
# def validate_document(doc, dtype):
#     """
#     Strict validation for document numbers based on type
#     Returns: (is_valid, error_message, risk_score)
#     """
#     doc = doc.strip()
    
#     if dtype == "AADHAR":
#         # AADHAR must be exactly 12 digits
#         if not doc.isdigit():
#             return False, "AADHAR must contain only digits", 0.85
#         if len(doc) != 12:
#             return False, f"AADHAR must be exactly 12 digits (got {len(doc)})", 0.80
#         # Check for patterns like 111111111111
#         if len(set(doc)) <= 3:
#             return False, "AADHAR contains suspicious repeated pattern", 0.90
#         return True, "", 0.15  # Valid AADHAR = low risk
    
#     elif dtype == "PAN":
#         # PAN format: 5 letters + 4 digits + 1 letter (e.g., ABCDE1234F)
#         if len(doc) != 10:
#             return False, f"PAN must be exactly 10 characters (got {len(doc)})", 0.75
#         if not (doc[:5].isalpha() and doc[5:9].isdigit() and doc[9].isalpha()):
#             return False, "PAN format should be: 5 letters + 4 digits + 1 letter", 0.80
#         if not doc.isupper():
#             return False, "PAN must be in uppercase", 0.70
#         return True, "", 0.18  # Valid PAN = low risk
    
#     elif dtype == "PASSPORT":
#         # Passport: Usually 8-9 alphanumeric characters
#         if len(doc) < 6 or len(doc) > 12:
#             return False, f"Passport number length invalid (got {len(doc)})", 0.70
#         if not doc.isalnum():
#             return False, "Passport should contain only letters and numbers", 0.75
#         return True, "", 0.20  # Valid passport = low risk
    
#     elif dtype == "UTILITY":
#         # Utility bills - more lenient
#         if len(doc) < 5:
#             return False, "Utility bill number too short", 0.65
#         return True, "", 0.25  # Valid utility = slightly higher baseline risk
    
#     else:
#         return False, f"Unknown document type: {dtype}", 0.80

# # ======================================
# # NAME & ADDRESS VALIDATION
# # ======================================
# def validate_name_address(name, address):
#     """
#     Validate name and address quality
#     Returns risk_adjustment (to add to base score)
#     """
#     risk_adj = 0.0
    
#     # Name validation
#     if not name or len(name.strip()) < 2:
#         risk_adj += 0.30  # No name = high risk
#     elif name.isdigit():
#         risk_adj += 0.50  # Name is all numbers = very suspicious
#     elif len(name.strip()) < 3:
#         risk_adj += 0.20  # Too short
#     elif len(name.split()) < 2:
#         risk_adj += 0.10  # No last name (slightly suspicious)
#     else:
#         risk_adj -= 0.05  # Full name = good
    
#     # Address validation
#     if not address or len(address.strip()) < 10:
#         risk_adj += 0.20  # Very short or no address
#     elif len(address.strip()) < 20:
#         risk_adj += 0.10  # Short address
#     else:
#         # Check if address has numbers (street numbers, pin codes)
#         if any(c.isdigit() for c in address):
#             risk_adj -= 0.05  # Detailed address = good
    
#     return risk_adj

# # ======================================
# # GNN FALLBACK - WITH STRICT VALIDATION
# # ======================================
# def gnn_pred(doc, name, address, dtype):
#     """
#     Enhanced GNN prediction with strict validation
#     """
#     try:
#         if not gnn_df.empty:
#             row = gnn_df[gnn_df["Document_Number"].astype(str) == str(doc)]
#             if not row.empty:
#                 return float(row.iloc[0]["GNN_Fraud_Probability"])
#     except Exception as e:
#         logger.warning(f"GNN lookup failed: {e}")
    
#     # First, validate the document
#     is_valid, error_msg, base_score = validate_document(doc, dtype)
    
#     if not is_valid:
#         logger.warning(f"Document validation failed: {error_msg}")
#         return base_score  # Return high risk score
    
#     # Document is valid, start with its base score (low risk)
#     score = base_score
    
#     # Add adjustments based on name and address
#     name_addr_risk = validate_name_address(name, address)
#     score += name_addr_risk
    
#     # Keep score in valid range (0.0 to 1.0)
#     score = max(0.0, min(1.0, score))
    
#     logger.info(f"Heuristic score for {doc} ({dtype}): {score:.2f}")
    
#     return score

# # ======================================
# # FULL PREDICTION - FIXED
# # ======================================
# def predict_fraud(name, doc, address, dtype):
#     """
#     Main prediction function with proper error handling and variance
#     """
#     X = extract_features(name, doc, address, dtype)
    
#     # Apply feature selector if available
#     if feature_selector:
#         try:
#             X = feature_selector.transform(X)
#         except Exception as e:
#             logger.warning(f"Feature selector failed: {e}")
    
#     # Apply scaler if available
#     if scaler:
#         try:
#             X = scaler.transform(X)
#         except Exception as e:
#             logger.warning(f"Scaler failed: {e}")
    
#     # Try model prediction
#     if model:
#         try:
#             proba_result = model.predict_proba(X)
            
#             # Handle different probability shapes
#             if proba_result.shape[1] == 2:
#                 prob = float(proba_result[0][1])  # Binary classification
#             elif proba_result.shape[1] == 1:
#                 prob = float(proba_result[0][0])
#             else:
#                 prob = float(proba_result[0][-1])
            
#             logger.info(f"Model prediction successful: {prob}")
            
#         except Exception as e:
#             logger.error(f"Model prediction failed: {e}, using heuristic fallback")
#             prob = gnn_pred(doc, name, address, dtype)
#     else:
#         logger.warning("Model not loaded, using heuristic scoring")
#         prob = gnn_pred(doc, name, address, dtype)
    
#     # Ensure probability is in valid range
#     prob = max(0.0, min(1.0, prob))
    
#     # Classify risk level
#     risk = classify(prob)
    
#     return {
#         "fraud_probability": round(prob * 100, 2),
#         "risk_level": risk,
#         "confidence": round((1 - prob) * 100, 2),
#         "status": "Flagged" if risk == "High" else "Verified"
#     }

# # ======================================
# # APP STARTUP
# # ======================================
# @app.on_event("startup")
# def startup_event():
#     logger.info("🚀 Booting API...")
#     ensure_gnn_csv()
#     load_models()
#     load_gnn()
#     logger.info("✅ Ready!")

# # ======================================
# # MAIN API ENDPOINT
# # ======================================
# @app.post("/api/verify-kyc", response_model=VerificationResponse)
# def verify(request: VerificationRequest):
#     result = predict_fraud(request.name, request.documentNumber, request.address, request.documentType)
#     vid = f"VER{int(datetime.datetime.now().timestamp() * 1000)}"
#     ts = datetime.datetime.now().isoformat()
    
#     # Log to audit
#     try:
#         df = pd.DataFrame([{
#             "Timestamp": ts,
#             "Name": request.name,
#             "ID_Type": request.documentType,
#             "Document_Number": request.documentNumber,
#             "Fraud_Risk": result["risk_level"],
#             "Fraud_Probability": result["fraud_probability"],
#         }])
#         df.to_csv(AUDIT_LOG, mode="a", header=not AUDIT_LOG.exists(), index=False)
#     except Exception as e:
#         logger.warning(f"⚠️ Could not write audit log: {e}")
    
#     return VerificationResponse(
#         status=result["status"],
#         id=vid,
#         timestamp=ts,
#         name=request.name,
#         documentNumber=request.documentNumber,
#         fraudProbability=result["fraud_probability"],
#         riskLevel=result["risk_level"],
#         confidence=result["confidence"],
#         details={
#             "documentAuthenticity": "Valid" if result["fraud_probability"] < 50 else "Suspicious",
#             "addressVerification": "Verified" if request.address and len(request.address) > 10 else "Pending",
#             "anomalyScore": f"{result['fraud_probability']:.2f}"
#         },
#         message="KYC processed successfully."
#     )

# # ======================================
# # ROOT CHECK
# # ======================================
# @app.get("/")
# def home():
#     return {
#         "message": "KYC API running",
#         "model": "Loaded" if model else "Not Loaded",
#         "scaler": "Loaded" if scaler else "Not Loaded",
#         "selector": "Loaded" if feature_selector else "Not Loaded",
#         "gnn_csv": "Available" if not gnn_df.empty else "Empty"
#     }

# # ======================================
# # DEBUG TEST PREDICTION
# # ======================================
# @app.get("/admin/test-prediction")
# def test_prediction():
#     test_cases = [
#         {"name": "John Doe", "doc": "123456789012", "address": "123 Main St, Springfield", "dtype": "AADHAR"},
#         {"name": "Jane Smith", "doc": "ABCDE1234F", "address": "456 Oak Ave, Metropolis", "dtype": "PAN"},
#         {"name": "Bob", "doc": "111111111", "address": "X", "dtype": "PASSPORT"},  # Suspicious case
#     ]
#     results = []
    
#     for test in test_cases:
#         result = predict_fraud(test["name"], test["doc"], test["address"], test["dtype"])
#         results.append({
#             "input": test,
#             "prediction": result
#         })
    
#     return {
#         "model_loaded": model is not None,
#         "scaler_loaded": scaler is not None,
#         "selector_loaded": feature_selector is not None,
#         "test_results": results
#     }

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import datetime
import os
import joblib
import numpy as np
from typing import Optional, List
import logging
from pathlib import Path
import io

# ======================================
# LOGGING
# ======================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

# ======================================
# FASTAPI SETUP
# ======================================
app = FastAPI(title="AI-Powered KYC Verification API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================
# PATHS
# ======================================
BASE_DIR = Path(__file__).parent
MODEL_PATH = BASE_DIR / "best_model.pkl"
SCALER_PATH = BASE_DIR / "scaler.pkl"
FEATURE_SELECTOR_PATH = BASE_DIR / "feature_selector.pkl"
GNN_CSV = BASE_DIR / "output_of_GNN_part2.csv"
AUDIT_LOG = BASE_DIR / "kyc_audit_log.csv"

# ======================================
# GLOBALS
# ======================================
model = None
scaler = None
feature_selector = None
gnn_df = pd.DataFrame()

# ======================================
# REQUEST MODELS
# ======================================
class VerificationRequest(BaseModel):
    name: str
    documentNumber: str
    address: Optional[str] = ""
    documentType: str  # PASSPORT / AADHAR / PAN

class VerificationResponse(BaseModel):
    status: str
    id: str
    timestamp: str
    name: str
    documentNumber: str
    fraudProbability: float
    riskLevel: str
    confidence: float
    details: dict
    message: str

class BatchResultItem(BaseModel):
    row: int
    name: str
    documentNumber: str
    address: str
    documentType: str
    status: str
    id: str
    timestamp: str
    fraudProbability: float
    riskLevel: str
    confidence: float
    details: dict
    message: str
    error: Optional[str] = None

class BatchVerificationResponse(BaseModel):
    total: int
    successful: int
    failed: int
    results: List[BatchResultItem]

# ======================================
# CREATE GNN CSV IF MISSING
# ======================================
def ensure_gnn_csv():
    if not GNN_CSV.exists():
        logger.warning("⚠️ Creating new GNN CSV file because it was missing.")
        df = pd.DataFrame({
            "Document_Number": [],
            "GNN_Fraud_Probability": []
        })
        df.to_csv(GNN_CSV, index=False)
        logger.info(f"✅ Created empty GNN CSV at {GNN_CSV}")

# ======================================
# LOAD MODELS
# ======================================
def load_models():
    global model, scaler, feature_selector
    try:
        model = joblib.load(MODEL_PATH)
        logger.info("✅ Loaded ML model")
    except Exception as e:
        logger.error(f"❌ Model load failed: {e}")
        model = None

    try:
        scaler = joblib.load(SCALER_PATH)
        logger.info("✅ Loaded scaler")
    except Exception as e:
        logger.error(f"❌ Scaler load failed: {e}")
        scaler = None

    try:
        feature_selector = joblib.load(FEATURE_SELECTOR_PATH)
        logger.info("✅ Loaded feature selector")
    except Exception as e:
        logger.error(f"❌ Feature selector load failed: {e}")
        feature_selector = None

# ======================================
# LOAD GNN OUTPUT CSV
# ======================================
def load_gnn():
    global gnn_df
    try:
        if not GNN_CSV.exists():
            logger.warning("⚠️ GNN CSV not found. Creating new...")
            ensure_gnn_csv()
        df = pd.read_csv(GNN_CSV)
        if df.empty:
            logger.warning("⚠️ GNN CSV is empty.")
            gnn_df = pd.DataFrame()
        else:
            gnn_df = df
            logger.info(f"✅ Loaded GNN CSV with {len(gnn_df)} rows")
    except Exception as e:
        logger.error(f"❌ Error loading GNN CSV: {e}")
        gnn_df = pd.DataFrame()

# ======================================
# FEATURE EXTRACTION - ENHANCED
# ======================================
def extract_features(name, doc, address, dtype):
    """
    Extract features with more variance to avoid constant predictions
    """
    # Basic features
    name_len = len(name)
    doc_len = len(doc)
    address_len = len(address)
    
    # Document validation
    doc_is_numeric = 1 if doc.isdigit() else 0
    doc_unique_chars = len(set(doc))
    
    # Document type encoding
    is_aadhar = 1 if dtype == "AADHAR" else 0
    is_pan = 1 if dtype == "PAN" else 0
    is_other = 1 if dtype in ["PASSPORT", "UTILITY"] else 0
    
    # Address analysis
    address_words = len(address.split())
    
    # Name analysis
    name_words = len(name.split())
    name_has_upper = 1 if any(x.isupper() for x in name) else 0
    name_has_digit = 1 if any(x.isdigit() for x in name) else 0
    
    # NEW: Additional variance features
    # Check for suspicious patterns
    has_repeated_chars = 1 if doc and len(set(doc)) < len(doc) * 0.5 else 0
    name_all_caps = 1 if name.isupper() else 0
    address_has_numbers = 1 if any(c.isdigit() for c in address) else 0
    
    features = [
        name_len,
        doc_len,
        address_len,
        doc_is_numeric,
        doc_unique_chars,
        is_aadhar,
        is_pan,
        is_other,
        address_words,
        name_words,
        name_has_upper,
        name_has_digit,
        has_repeated_chars,
        name_all_caps,
        address_has_numbers,
    ]
    
    return np.array(features).reshape(1, -1)

# ======================================
# RISK LABEL
# ======================================
def classify(prob):
    if prob < 0.33:
        return "Low"
    elif prob < 0.67:
        return "Medium"
    return "High"

# ======================================
# DOCUMENT VALIDATION
# ======================================
def validate_document(doc, dtype):
    """
    Strict validation for document numbers based on type
    Returns: (is_valid, error_message, risk_score)
    """
    doc = doc.strip()
    
    if dtype == "AADHAR":
        # AADHAR must be exactly 12 digits
        if not doc.isdigit():
            return False, "AADHAR must contain only digits", 0.85
        if len(doc) != 12:
            return False, f"AADHAR must be exactly 12 digits (got {len(doc)})", 0.80
        # Check for patterns like 111111111111
        if len(set(doc)) <= 3:
            return False, "AADHAR contains suspicious repeated pattern", 0.90
        return True, "", 0.15  # Valid AADHAR = low risk
    
    elif dtype == "PAN":
        # PAN format: 5 letters + 4 digits + 1 letter (e.g., ABCDE1234F)
        if len(doc) != 10:
            return False, f"PAN must be exactly 10 characters (got {len(doc)})", 0.75
        if not (doc[:5].isalpha() and doc[5:9].isdigit() and doc[9].isalpha()):
            return False, "PAN format should be: 5 letters + 4 digits + 1 letter", 0.80
        if not doc.isupper():
            return False, "PAN must be in uppercase", 0.70
        return True, "", 0.18  # Valid PAN = low risk
    
    elif dtype == "PASSPORT":
        # Passport: Usually 8-9 alphanumeric characters
        if len(doc) < 6 or len(doc) > 12:
            return False, f"Passport number length invalid (got {len(doc)})", 0.70
        if not doc.isalnum():
            return False, "Passport should contain only letters and numbers", 0.75
        return True, "", 0.20  # Valid passport = low risk
    
    elif dtype == "UTILITY":
        # Utility bills - more lenient
        if len(doc) < 5:
            return False, "Utility bill number too short", 0.65
        return True, "", 0.25  # Valid utility = slightly higher baseline risk
    
    else:
        return False, f"Unknown document type: {dtype}", 0.80

# ======================================
# NAME & ADDRESS VALIDATION
# ======================================
def validate_name_address(name, address):
    """
    Validate name and address quality
    Returns risk_adjustment (to add to base score)
    """
    risk_adj = 0.0
    
    # Name validation
    if not name or len(name.strip()) < 2:
        risk_adj += 0.30  # No name = high risk
    elif name.isdigit():
        risk_adj += 0.50  # Name is all numbers = very suspicious
    elif len(name.strip()) < 3:
        risk_adj += 0.20  # Too short
    elif len(name.split()) < 2:
        risk_adj += 0.10  # No last name (slightly suspicious)
    else:
        risk_adj -= 0.05  # Full name = good
    
    # Address validation
    if not address or len(address.strip()) < 10:
        risk_adj += 0.20  # Very short or no address
    elif len(address.strip()) < 20:
        risk_adj += 0.10  # Short address
    else:
        # Check if address has numbers (street numbers, pin codes)
        if any(c.isdigit() for c in address):
            risk_adj -= 0.05  # Detailed address = good
    
    return risk_adj

# ======================================
# GNN FALLBACK - WITH STRICT VALIDATION
# ======================================
def gnn_pred(doc, name, address, dtype):
    """
    Enhanced GNN prediction with strict validation
    """
    try:
        if not gnn_df.empty:
            row = gnn_df[gnn_df["Document_Number"].astype(str) == str(doc)]
            if not row.empty:
                return float(row.iloc[0]["GNN_Fraud_Probability"])
    except Exception as e:
        logger.warning(f"GNN lookup failed: {e}")
    
    # First, validate the document
    is_valid, error_msg, base_score = validate_document(doc, dtype)
    
    if not is_valid:
        logger.warning(f"Document validation failed: {error_msg}")
        return base_score  # Return high risk score
    
    # Document is valid, start with its base score (low risk)
    score = base_score
    
    # Add adjustments based on name and address
    name_addr_risk = validate_name_address(name, address)
    score += name_addr_risk
    
    # Keep score in valid range (0.0 to 1.0)
    score = max(0.0, min(1.0, score))
    
    logger.info(f"Heuristic score for {doc} ({dtype}): {score:.2f}")
    
    return score

# ======================================
# FULL PREDICTION - FIXED
# ======================================
def predict_fraud(name, doc, address, dtype):
    """
    Main prediction function with proper error handling and variance
    """
    X = extract_features(name, doc, address, dtype)
    
    # Apply feature selector if available
    if feature_selector:
        try:
            X = feature_selector.transform(X)
        except Exception as e:
            logger.warning(f"Feature selector failed: {e}")
    
    # Apply scaler if available
    if scaler:
        try:
            X = scaler.transform(X)
        except Exception as e:
            logger.warning(f"Scaler failed: {e}")
    
    # Try model prediction
    if model:
        try:
            proba_result = model.predict_proba(X)
            
            # Handle different probability shapes
            if proba_result.shape[1] == 2:
                prob = float(proba_result[0][1])  # Binary classification
            elif proba_result.shape[1] == 1:
                prob = float(proba_result[0][0])
            else:
                prob = float(proba_result[0][-1])
            
            logger.info(f"Model prediction successful: {prob}")
            
        except Exception as e:
            logger.error(f"Model prediction failed: {e}, using heuristic fallback")
            prob = gnn_pred(doc, name, address, dtype)
    else:
        logger.warning("Model not loaded, using heuristic scoring")
        prob = gnn_pred(doc, name, address, dtype)
    
    # Ensure probability is in valid range
    prob = max(0.0, min(1.0, prob))
    
    # Classify risk level
    risk = classify(prob)
    
    return {
        "fraud_probability": round(prob * 100, 2),
        "risk_level": risk,
        "confidence": round((1 - prob) * 100, 2),
        "status": "Flagged" if risk == "High" else "Verified"
    }

# ======================================
# APP STARTUP
# ======================================
@app.on_event("startup")
def startup_event():
    logger.info("🚀 Booting API...")
    ensure_gnn_csv()
    load_models()
    load_gnn()
    logger.info("✅ Ready!")

# ======================================
# MAIN API ENDPOINT
# ======================================
@app.post("/api/verify-kyc", response_model=VerificationResponse)
def verify(request: VerificationRequest):
    result = predict_fraud(request.name, request.documentNumber, request.address, request.documentType)
    vid = f"VER{int(datetime.datetime.now().timestamp() * 1000)}"
    ts = datetime.datetime.now().isoformat()
    
    # Log to audit
    try:
        df = pd.DataFrame([{
            "Timestamp": ts,
            "Name": request.name,
            "ID_Type": request.documentType,
            "Document_Number": request.documentNumber,
            "Fraud_Risk": result["risk_level"],
            "Fraud_Probability": result["fraud_probability"],
        }])
        df.to_csv(AUDIT_LOG, mode="a", header=not AUDIT_LOG.exists(), index=False)
    except Exception as e:
        logger.warning(f"⚠️ Could not write audit log: {e}")
    
    return VerificationResponse(
        status=result["status"],
        id=vid,
        timestamp=ts,
        name=request.name,
        documentNumber=request.documentNumber,
        fraudProbability=result["fraud_probability"],
        riskLevel=result["risk_level"],
        confidence=result["confidence"],
        details={
            "documentAuthenticity": "Valid" if result["fraud_probability"] < 50 else "Suspicious",
            "addressVerification": "Verified" if request.address and len(request.address) > 10 else "Pending",
            "anomalyScore": f"{result['fraud_probability']:.2f}"
        },
        message="KYC processed successfully."
    )

# ======================================
# ROOT CHECK
# ======================================
@app.get("/")
def home():
    return {
        "message": "KYC API running",
        "model": "Loaded" if model else "Not Loaded",
        "scaler": "Loaded" if scaler else "Not Loaded",
        "selector": "Loaded" if feature_selector else "Not Loaded",
        "gnn_csv": "Available" if not gnn_df.empty else "Empty"
    }

# ======================================
# BATCH CSV UPLOAD ENDPOINT
# ======================================
@app.post("/api/batch-verify", response_model=BatchVerificationResponse)
async def batch_verify(file: UploadFile = File(...)):
    """
    Upload a CSV file for batch KYC verification
    Expected CSV columns: name, documentNumber, address, documentType
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    try:
        # Read CSV file
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        # Validate required columns
        required_cols = ['name', 'documentNumber', 'documentType']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise HTTPException(
                status_code=400, 
                detail=f"Missing required columns: {', '.join(missing_cols)}"
            )
        
        # Add address column if missing
        if 'address' not in df.columns:
            df['address'] = ""
        
        # Process each row
        results = []
        successful = 0
        failed = 0
        
        for idx, row in df.iterrows():
            try:
                # Extract data
                name = str(row.get('name', ''))
                doc_num = str(row.get('documentNumber', ''))
                address = str(row.get('address', ''))
                doc_type = str(row.get('documentType', 'AADHAR'))
                
                # Make prediction
                result = predict_fraud(name, doc_num, address, doc_type)
                
                # Generate ID and timestamp
                vid = f"VER{int(datetime.datetime.now().timestamp() * 1000)}_{idx}"
                ts = datetime.datetime.now().isoformat()
                
                # Create result item
                results.append(BatchResultItem(
                    row=idx + 1,
                    name=name,
                    documentNumber=doc_num,
                    address=address,
                    documentType=doc_type,
                    status=result["status"],
                    id=vid,
                    timestamp=ts,
                    fraudProbability=result["fraud_probability"],
                    riskLevel=result["risk_level"],
                    confidence=result["confidence"],
                    details={
                        "documentAuthenticity": "Valid" if result["fraud_probability"] < 50 else "Suspicious",
                        "addressVerification": "Verified" if address and len(address) > 10 else "Pending",
                        "anomalyScore": f"{result['fraud_probability']:.2f}"
                    },
                    message="KYC processed successfully.",
                    error=None
                ))
                successful += 1
                
            except Exception as e:
                logger.error(f"Error processing row {idx}: {e}")
                results.append(BatchResultItem(
                    row=idx + 1,
                    name=str(row.get('name', '')),
                    documentNumber=str(row.get('documentNumber', '')),
                    address=str(row.get('address', '')),
                    documentType=str(row.get('documentType', 'AADHAR')),
                    status="Error",
                    id=f"ERR{idx}",
                    timestamp=datetime.datetime.now().isoformat(),
                    fraudProbability=0.0,
                    riskLevel="Unknown",
                    confidence=0.0,
                    details={},
                    message="Processing failed",
                    error=str(e)
                ))
                failed += 1
        
        # Log batch to audit
        try:
            audit_df = pd.DataFrame([{
                "Timestamp": datetime.datetime.now().isoformat(),
                "Name": r.name,
                "ID_Type": r.documentType,
                "Document_Number": r.documentNumber,
                "Fraud_Risk": r.riskLevel,
                "Fraud_Probability": r.fraudProbability,
            } for r in results if r.error is None])
            
            audit_df.to_csv(AUDIT_LOG, mode="a", header=not AUDIT_LOG.exists(), index=False)
        except Exception as e:
            logger.warning(f"Could not write batch audit log: {e}")
        
        return BatchVerificationResponse(
            total=len(results),
            successful=successful,
            failed=failed,
            results=results
        )
        
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="CSV file is empty")
    except Exception as e:
        logger.error(f"Batch verification error: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")

# ======================================
# DEBUG TEST PREDICTION
# ======================================
@app.get("/admin/test-prediction")
def test_prediction():
    test_cases = [
        {"name": "John Doe", "doc": "123456789012", "address": "123 Main St, Springfield", "dtype": "AADHAR"},
        {"name": "Jane Smith", "doc": "ABCDE1234F", "address": "456 Oak Ave, Metropolis", "dtype": "PAN"},
        {"name": "Bob", "doc": "111111111", "address": "X", "dtype": "PASSPORT"},  # Suspicious case
    ]
    results = []
    
    for test in test_cases:
        result = predict_fraud(test["name"], test["doc"], test["address"], test["dtype"])
        results.append({
            "input": test,
            "prediction": result
        })
    
    return {
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None,
        "selector_loaded": feature_selector is not None,
        "test_results": results
    }