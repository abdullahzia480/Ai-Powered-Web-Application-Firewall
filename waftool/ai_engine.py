import joblib
import os

class AIEngine:
    def __init__(self, model_filename='firewall_model.pkl'):
        # Get directory of this script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, model_filename)

        if not os.path.exists(model_path):
             raise FileNotFoundError(f"Model file not found at {model_path}. Please run model_trainer.py first.")
        self.model = joblib.load(model_path)

    def predict(self, text):
        """
        Predicts if the text is malicious.
        Returns a tuple (is_malicious, risk_score)
        """
        # The model expects a list/iterable
        prediction = self.model.predict([text])[0]
        # Get probability (risk score)
        # probability of class 1 (malicious)
        proba = self.model.predict_proba([text])[0][1] 
        
        is_malicious = True if prediction == 1 else False
        
        # You can add a threshold override here if needed, 
        # but the model prediction is based on 0.5 usually.
        
        return is_malicious, proba
