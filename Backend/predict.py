import joblib
import os
import numpy as np

# ============================
# MODEL FILE PATHS
# ============================
MODEL_PATH = "best_model.pkl"
SCALER_PATH = "scaler.pkl"
SELECTOR_PATH = "feature_selector.pkl"

# ============================
# LOAD MODELS
# ============================
model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None
scaler = joblib.load(SCALER_PATH) if os.path.exists(SCALER_PATH) else None
selector = joblib.load(SELECTOR_PATH) if os.path.exists(SELECTOR_PATH) else None


# ============================
# FEATURE ENGINEERING (SAME AS MAIN BACKEND)
# ============================
def extract_features(name, doc_number, address, doc_type):
    features = []

    features.append(len(name))
    features.append(len(doc_number))
    features.append(len(address))

    features.append(1 if doc_number.isdigit() else 0)
    features.append(len(set(doc_number)))

    doc_map = {"AADHAR": 0, "PAN": 1, "UTILITY": 2}
    onehot = [0, 0, 0]
    if doc_type in doc_map:
        onehot[doc_map[doc_type]] = 1
    features.extend(onehot)

    features.append(len(address.split()))
    features.append(len(name.split()))
    features.append(1 if any(x.isupper() for x in name) else 0)
    features.append(1 if any(x.isdigit() for x in name) else 0)

    return np.array(features).reshape(1, -1)


# ============================
# RISK CLASSIFICATION
# ============================
def classify_risk(prob):
    if prob < 33:
        return "Low"
    elif prob < 66:
        return "Medium"
    return "High"


# ============================
# MAIN PREDICTION FUNCTION
# ============================
def run_model_prediction(
    name="Test User",
    doc_number="123456789",
    address="Sample address 123",
    doc_type="AADHAR"
):
    """
    Runs a test prediction for debugging or integration.
    """

    # Step 1: Extract features
    X = extract_features(name, doc_number, address, doc_type)

    # Step 2: Selector
    if selector is not None:
        X = selector.transform(X)

    # Step 3: Scaler
    if scaler is not None:
        X = scaler.transform(X)

    # Step 4: Prediction
    if model is None:
        raise ValueError("Model not loaded. Please ensure best_model.pkl exists.")
    
    # Type narrowing: model is guaranteed to be not None after the check above
    assert model is not None, "Model should not be None at this point"
    
    if hasattr(model, "predict_proba"):
        prob = model.predict_proba(X)[0][1] * 100
    else:
        pred = model.predict(X)[0]
        prob = 80 if pred == 1 else 20

    prob = round(prob, 2)
    risk = classify_risk(prob)
    confidence = round(100 - prob, 2)

    return {
        "fraud_probability": prob,
        "fraud_risk": risk,
        "confidence": confidence
    }


# ============================
# DEBUG RUN
# ============================
if __name__ == "__main__":
    print(run_model_prediction())
