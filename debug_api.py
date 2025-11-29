#!/usr/bin/env python3
"""Debug script to test API imports and services"""
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

print("Testing imports...")

try:
    print("1. Importing config...")
    from app.config import get_settings
    settings = get_settings()
    print(f"   ✅ Config loaded")
    print(f"   - OpenAI Key: {'SET' if settings.openai_api_key else 'NOT SET'}")

    print("\n2. Importing DataLoader...")
    from app.utils.data_loader import DataLoader
    print("   ✅ DataLoader imported")

    print("\n3. Creating DataLoader instance...")
    loader = DataLoader()
    print("   ✅ DataLoader created")

    print("\n4. Loading Salesforce data...")
    sf_data = loader.load_salesforce_data()
    print(f"   ✅ Salesforce data loaded: {len(sf_data['accounts'])} accounts")

    print("\n5. Importing AIService...")
    from app.services.ai_service import AIService
    print("   ✅ AIService imported")

    print("\n6. Creating AIService instance...")
    ai_service = AIService()
    print("   ✅ AIService created")

    print("\n7. Importing IntelligenceService...")
    from app.services.intelligence_service import IntelligenceService
    print("   ✅ IntelligenceService imported")

    print("\n8. Creating IntelligenceService instance...")
    intel_service = IntelligenceService(loader, ai_service)
    print("   ✅ IntelligenceService created")

    print("\n9. Testing get_client_info...")
    client = intel_service.get_client_info("GreenTech")
    if client:
        print(f"   ✅ Found client: {client['account'].get('Name')}")
    else:
        print("   ⚠️  Client not found")

    print("\n✅ All tests passed!")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
