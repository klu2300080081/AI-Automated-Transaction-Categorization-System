import joblib
import os
import sys

# Add parent directory to path to find SafeTransactionPipeline
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import SafeTransactionPipeline BEFORE loading the pickle
from SafeTransactionPipeline import SafeTransactionPipeline

class PredictionService:
    
    def __init__(self, model_path: str = "full_pipeline.pkl"):
        # Construct full path to model file in root directory
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.model_path = os.path.join(root_dir, model_path)
        self.pipeline = None
        self._load_model()
    
    def _load_model(self):
        try:
            if os.path.exists(self.model_path):
                self.pipeline = joblib.load(self.model_path)
                return True
            else:
                print(f"Model file not found at {self.model_path}")
                return False
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def predict_transaction(self, merchant: str, timestamp: str) -> dict:
        try:
            if self.pipeline is None:
                return {
                    "success": False,
                    "message": "Model not loaded"
                }
            
            result = self.pipeline.predict(
                merchant=merchant,
                timestamp=timestamp
            )
            
            return {
                "success": True,
                "result": result
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Prediction error: {str(e)}"
            }
    
    def is_model_loaded(self) -> bool:
        return self.pipeline is not None