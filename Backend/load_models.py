import joblib
from pathlib import Path

BASE_DIR = Path(__file__).parent

def load_all_models():
    models = {}

    try:
        models["model"] = joblib.load(BASE_DIR / "best_model.pkl")
        print("✅ best_model.pkl loaded")

        models["selector"] = joblib.load(BASE_DIR / "feature_selector.pkl")
        print("✅ feature_selector.pkl loaded")

        models["scaler"] = joblib.load(BASE_DIR / "scaler.pkl")
        print("✅ scaler.pkl loaded")

        models["gnn_output"] = joblib.load(BASE_DIR / "output_of_GNN_model.pkl")
        print("✅ output_of_GNN_model.pkl loaded")

    except Exception as e:
        print("❌ Error loading model:", e)

    return models
