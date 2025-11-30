from src.domain.interfaces.i_classifier import IClassifier
import joblib
import os

MODEL_PATH = os.path.join("models", "fake_model.pkl")
VECT_PATH = os.path.join("models", "vectorizer.pkl")

class MLClassifier(IClassifier):
    def __init__(self):
        try:
            self.model = joblib.load(MODEL_PATH)
            self.vectorizer = joblib.load(VECT_PATH)
        except Exception:
            self.model = None
            self.vectorizer = None

    def classify(self, text: str) -> float:
        if not self.model or not self.vectorizer:
            # fallback neutro
            return 0.0
        X = self.vectorizer.transform([text])
        return float(self.model.predict_proba(X)[0][1])
