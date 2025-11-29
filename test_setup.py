#!/usr/bin/env python3
"""Quick setup verification script"""
import sys
from pathlib import Path


def check_data_files():
    """Check if data files exist"""
    print("🔍 Checking data files...")

    base_path = Path("..").resolve()
    checks = {
        "Salesforce": base_path / "hackathon_fake_salesforce" / "Accounts.csv",
        "SharePoint": base_path / "hackathon_fake_sharepoint_news" / "news_feed" / "NewsFeed.json",
        "Knowledge Hub": base_path / "hackathon_extra_calendar_knowledge_regulatory" / "knowledge_hub",
    }

    all_good = True
    for name, path in checks.items():
        if path.exists():
            print(f"  ✅ {name}: {path}")
        else:
            print(f"  ❌ {name}: NOT FOUND at {path}")
            all_good = False

    return all_good


def check_env_file():
    """Check if .env is configured"""
    print("\n🔍 Checking environment configuration...")

    env_file = Path(".env")

    if not env_file.exists():
        print("  ❌ .env file not found")
        print("  💡 Copy .env.example to .env and add your OpenAI API key")
        return False

    with open(env_file) as f:
        content = f.read()

    if "OPENAI_API_KEY=sk-" in content:
        print("  ✅ OPENAI_API_KEY is configured")
        return True
    else:
        print("  ❌ OPENAI_API_KEY not configured in .env")
        print("  💡 Edit .env and add: OPENAI_API_KEY=sk-your-key-here")
        return False


def check_dependencies():
    """Check if key dependencies are installed"""
    print("\n🔍 Checking dependencies...")

    deps = [
        "fastapi",
        "uvicorn",
        "openai",
        "pandas",
        "pydantic_settings",
    ]

    all_good = True
    for dep in deps:
        try:
            __import__(dep)
            print(f"  ✅ {dep}")
        except ImportError:
            print(f"  ❌ {dep} not installed")
            all_good = False

    return all_good


def test_data_loading():
    """Test if data can be loaded"""
    print("\n🔍 Testing data loading...")

    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from app.utils.data_loader import DataLoader

        loader = DataLoader()

        # Test Salesforce data
        sf_data = loader.load_salesforce_data()
        print(f"  ✅ Salesforce: {len(sf_data['accounts'])} accounts loaded")

        # Test knowledge hub
        knowledge = loader.load_knowledge_hub()
        print(f"  ✅ Knowledge Hub: {len(knowledge)} documents loaded")

        # Test news feed
        news = loader.load_news_feed()
        print(f"  ✅ News Feed: {len(news)} items loaded")

        return True

    except Exception as e:
        print(f"  ❌ Error loading data: {e}")
        return False


def main():
    """Run all checks"""
    print("=" * 60)
    print("Meeting Prep Assistant - Setup Verification")
    print("=" * 60)

    checks = [
        ("Data Files", check_data_files),
        ("Environment", check_env_file),
        ("Dependencies", check_dependencies),
        ("Data Loading", test_data_loading),
    ]

    results = []
    for name, check_func in checks:
        result = check_func()
        results.append((name, result))

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
        if not passed:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n🎉 All checks passed! You're ready to go!")
        print("\nNext steps:")
        print("  1. Run the API: ./run.sh")
        print("  2. Visit: http://localhost:8000/docs")
        print("  3. Try the examples in API_EXAMPLES.md")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
