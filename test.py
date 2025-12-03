import joblib
from SafeTransactionPipeline import SafeTransactionPipeline

pipeline = joblib.load("full_pipeline.pkl")

result = pipeline.predict(
    merchant="Starbucks Mumbai #221",
    timestamp="2025-01-10 09:30:00"
)

print(result)
    