import numpy as np
import joblib
import pandas as pd
import os

MODEL_DIR = "model/"

scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
features = joblib.load(os.path.join(MODEL_DIR, "features.pkl"))


def preprocess_dummy_input():
    """
    This function PREPARES dummy values because you are not passing
    tabular inputs from frontend yet.
    """
    df = pd.DataFrame([[0] * len(features)], columns=features)
    scaled = scaler.transform(df)
    return scaled
