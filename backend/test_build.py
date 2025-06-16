"""
Simple test script to validate the build environment
This script tests basic functionality before attempting full Nuitka compilation
"""

import sys
import importlib
from pathlib import Path

def test_python_version():
    """Test Python version compatibility"""
    print(f"Python version: {sys.version}")
    
    version_info = sys.version_info
    if version_info.major != 3 or version_info.minor < 11:
        print("❌ Python 3.11+ required")
        return False
    
    print("✅ Python version compatible")
    return True


def test_required_packages():
    """Test that all required packages can be imported"""
    required_packages = [
        "fastapi",
        "uvicorn", 
        "pydantic",
        "requests",
        "bs4",  # beautifulsoup4
        "docx",  # python-docx
        "pypdf",
        "loguru",
        "spacy",
        "nuitka"
    ]
    
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\nFailed to import: {', '.join(failed_imports)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True


def test_spacy_model():
    """Test spaCy model loading"""
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        
        # Test basic functionality
        doc = nlp("This is a test sentence with Python programming skills.")
        tokens = [token.text for token in doc]
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        
        print("✅ spaCy model loaded successfully")
        print(f"   Tokens: {len(tokens)}")
        print(f"   Entities: {entities}")
        return True
        
    except OSError:
        print("❌ spaCy model 'en_core_web_sm' not found")
        print("   Run: python -m spacy download en_core_web_sm")
        return False
    except Exception as e:
        print(f"❌ spaCy error: {e}")
        return False


def test_fastapi_basic():
    """Test FastAPI basic functionality"""
    try:
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        
        app = FastAPI()
        
        @app.get("/test")
        def test_endpoint():
            return {"status": "ok"}
        
        client = TestClient(app)
        response = client.get("/test")
        
        if response.status_code == 200 and response.json()["status"] == "ok":
            print("✅ FastAPI basic functionality working")
            return True
        else:
            print("❌ FastAPI test failed")
            return False
            
    except Exception as e:
        print(f"❌ FastAPI error: {e}")
        return False


def test_document_processing():
    """Test document processing capabilities"""
    try:
        # Test python-docx
        from docx import Document
        doc = Document()
        doc.add_paragraph("Test paragraph")
        print("✅ python-docx working")
        
        # Test pypdf
        import pypdf
        print("✅ pypdf working")
        
        return True
        
    except Exception as e:
        print(f"❌ Document processing error: {e}")
        return False


def test_web_scraping():
    """Test web scraping capabilities"""
    try:
        import requests
        from bs4 import BeautifulSoup
        import trafilatura
        
        # Simple test
        html = "<html><body><p>Test content</p></body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        
        if "Test content" in text:
            print("✅ Web scraping libraries working")
            return True
        else:
            print("❌ Web scraping test failed")
            return False
            
    except Exception as e:
        print(f"❌ Web scraping error: {e}")
        return False


def main():
    """Run all tests"""
    print("=== Resume Analyzer Build Environment Test ===\n")
    
    tests = [
        ("Python Version", test_python_version),
        ("Required Packages", test_required_packages),
        ("spaCy Model", test_spacy_model),
        ("FastAPI Basic", test_fastapi_basic),
        ("Document Processing", test_document_processing),
        ("Web Scraping", test_web_scraping),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print(f"\n=== Results: {passed}/{total} tests passed ===")
    
    if passed == total:
        print("🎉 All tests passed! Build environment is ready.")
        return True
    else:
        print("❌ Some tests failed. Please fix the issues before building.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
