import os
import sys

print("🔍 DIAGNOSTIC REPORT")
print("=" * 60)

# Check current directory
current_dir = os.getcwd()
print(f"\n📂 Current Directory:\n   {current_dir}")

# Check if critical files exist
print("\n📄 Critical Files Check:")
critical_files = [
    "SafeTransactionPipeline.py",
    "full_pipeline.pkl",
    "taxonomy.json",
    "app.py",
    ".env"
]

for file in critical_files:
    full_path = os.path.join(current_dir, file)
    exists = os.path.exists(full_path)
    status = "✅" if exists else "❌"
    print(f"   {status} {file}")
    if exists:
        print(f"      Path: {full_path}")

# Check directories
print("\n📁 Required Directories:")
dirs = ["config", "services", "utils", "styles", "pages"]
for dir_name in dirs:
    full_path = os.path.join(current_dir, dir_name)
    exists = os.path.isdir(full_path)
    status = "✅" if exists else "❌"
    print(f"   {status} {dir_name}/")

# Check services directory contents
services_dir = os.path.join(current_dir, "services")
if os.path.isdir(services_dir):
    print("\n📦 Services Directory Contents:")
    for file in os.listdir(services_dir):
        print(f"   - {file}")

# Try importing SafeTransactionPipeline
print("\n🐍 Import Test:")
print(f"   Python Path (first 3):")
for p in sys.path[:3]:
    print(f"      {p}")

try:
    from SafeTransactionPipeline import SafeTransactionPipeline
    print("   ✅ SafeTransactionPipeline imported successfully!")
except ImportError as e:
    print(f"   ❌ Import failed: {e}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Check Python version
print(f"\n🐍 Python Version: {sys.version}")

# Try loading the model
print("\n📦 Model Loading Test:")
try:
    import joblib
    from SafeTransactionPipeline import SafeTransactionPipeline
    
    model_path = os.path.join(current_dir, "full_pipeline.pkl")
    if os.path.exists(model_path):
        print(f"   Model file found at: {model_path}")
        pipeline = joblib.load(model_path)
        print("   ✅ Model loaded successfully!")
        
        # Test prediction
        result = pipeline.predict(
            merchant="Test Store",
            timestamp="2025-01-10 09:30:00"
        )
        print(f"   ✅ Test prediction successful!")
        print(f"      Category: {result['predicted_category']}")
    else:
        print(f"   ❌ Model file not found at: {model_path}")
except Exception as e:
    print(f"   ❌ Model loading failed: {e}")

print("\n" + "=" * 60)
print("\n💡 SOLUTION:")
print("   If SafeTransactionPipeline import failed, make sure:")
print("   1. SafeTransactionPipeline.py is in the ROOT directory")
print("   2. You're running this script from the ROOT directory")
print("   3. The file name is spelled correctly (case-sensitive)")
print("\n   Run this command from your project root:")
print("   python check_setup.py")