from datetime import datetime
from config.db_config import db_config
import uuid

class TransactionService:
    
    def __init__(self):
        self.db = db_config.get_database()
        self.transactions_collection = self.db["transactions"]
        self.feedback_collection = self.db["feedback"]
        self._create_indexes()
    
    def _create_indexes(self):
        self.transactions_collection.create_index("user_id")
        self.transactions_collection.create_index("timestamp")
        self.feedback_collection.create_index("user_id")
    
    def save_transaction(self, user_id: str, merchant: str, timestamp: str, 
                        category: str, confidence: float, raw_scores: list) -> dict:
        try:
            transaction_data = {
                "transaction_id": str(uuid.uuid4()),
                "user_id": user_id,
                "merchant": merchant,
                "timestamp": timestamp,
                "category": category,
                "confidence": confidence,
                "raw_scores": raw_scores,
                "created_at": datetime.utcnow()
            }
            
            result = self.transactions_collection.insert_one(transaction_data)
            
            return {
                "success": True,
                "message": "Transaction saved successfully",
                "transaction_id": transaction_data["transaction_id"]
            }
        
        except Exception as e:
            return {"success": False, "message": f"Error saving transaction: {str(e)}"}
    
    def get_user_transactions(self, user_id: str, limit: int = 100) -> list:
        try:
            transactions = self.transactions_collection.find(
                {"user_id": user_id},
                {"_id": 0}
            ).sort("created_at", -1).limit(limit)
            
            return list(transactions)
        
        except Exception as e:
            print(f"Error fetching transactions: {e}")
            return []
    
    def save_feedback(self, user_id: str, merchant: str, actual_category: str, 
                     transaction_id: str = None) -> dict:
        try:
            feedback_data = {
                "feedback_id": str(uuid.uuid4()),
                "user_id": user_id,
                "merchant": merchant,
                "actual_category": actual_category,
                "transaction_id": transaction_id,
                "created_at": datetime.utcnow()
            }
            
            self.feedback_collection.insert_one(feedback_data)
            
            return {
                "success": True,
                "message": "Feedback saved successfully"
            }
        
        except Exception as e:
            return {"success": False, "message": f"Error saving feedback: {str(e)}"}
    
    def get_transaction_stats(self, user_id: str) -> dict:
        try:
            total_transactions = self.transactions_collection.count_documents({"user_id": user_id})
            
            # Category distribution
            pipeline = [
                {"$match": {"user_id": user_id}},
                {"$group": {"_id": "$category", "count": {"$sum": 1}}}
            ]
            
            category_dist = list(self.transactions_collection.aggregate(pipeline))
            
            return {
                "total_transactions": total_transactions,
                "category_distribution": category_dist
            }
        
        except Exception as e:
            print(f"Error fetching stats: {e}")
            return {"total_transactions": 0, "category_distribution": []}