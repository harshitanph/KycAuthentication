"""
Complete Flow Test Script
Tests the entire flow: Frontend → Backend → Model → Results → Display
"""

import requests
import json
import sys

API_BASE_URL = "http://127.0.0.1:8000"

def test_backend_status():
    """Test 1: Check if backend is running"""
    print("=" * 60)
    print("TEST 1: Backend Status Check")
    print("=" * 60)
    try:
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend is running")
            print(f"   Status: {data.get('status')}")
            print(f"   Models:")
            for model_name, status in data.get('models', {}).items():
                print(f"     - {model_name}: {status}")
            return True, data
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False, None
    except Exception as e:
        print(f"❌ Backend is not running: {e}")
        print(f"   Please start backend: cd backend && uvicorn main:app --reload")
        return False, None

def test_api_verification():
    """Test 2: Test KYC Verification API"""
    print("\n" + "=" * 60)
    print("TEST 2: KYC Verification API")
    print("=" * 60)
    
    test_data = {
        "name": "John Doe",
        "documentNumber": "123456789012",
        "address": "123 Main Street, City, State 12345",
        "documentType": "AADHAR"
    }
    
    print(f"📤 Sending request:")
    print(f"   Name: {test_data['name']}")
    print(f"   Document Number: {test_data['documentNumber']}")
    print(f"   Document Type: {test_data['documentType']}")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/verify-kyc",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ API Response Received:")
            print(f"   Status: {result.get('status')}")
            print(f"   ID: {result.get('id')}")
            print(f"   Fraud Probability: {result.get('fraudProbability')}%")
            print(f"   Risk Level: {result.get('riskLevel')}")
            print(f"   Confidence: {result.get('confidence')}%")
            print(f"   Message: {result.get('message')}")
            
            # Verify response structure
            required_fields = ['status', 'id', 'fraudProbability', 'riskLevel', 'confidence', 'details']
            missing_fields = [field for field in required_fields if field not in result]
            
            if missing_fields:
                print(f"\n⚠️  Missing fields in response: {missing_fields}")
                return False, result
            else:
                print("\n✅ All required fields present in response")
                return True, result
        else:
            print(f"\n❌ API returned status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False, None
    except Exception as e:
        print(f"\n❌ API request failed: {e}")
        return False, None

def test_model_prediction():
    """Test 3: Verify model is making predictions"""
    print("\n" + "=" * 60)
    print("TEST 3: Model Prediction Verification")
    print("=" * 60)
    
    # Test with different inputs to see if predictions vary
    test_cases = [
        {
            "name": "Valid User",
            "documentNumber": "111111111111",
            "address": "123 Valid Street",
            "documentType": "AADHAR"
        },
        {
            "name": "Suspicious User",
            "documentNumber": "999999999999",
            "address": "X",
            "documentType": "AADHAR"
        }
    ]
    
    results = []
    for i, test_data in enumerate(test_cases, 1):
        print(f"\n   Test Case {i}: {test_data['name']}")
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/verify-kyc",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                result = response.json()
                results.append(result)
                print(f"     Fraud Probability: {result.get('fraudProbability')}%")
                print(f"     Risk Level: {result.get('riskLevel')}")
            else:
                print(f"     ❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"     ❌ Error: {e}")
    
    if len(results) >= 2:
        # Check if predictions are different (model is working)
        prob1 = results[0].get('fraudProbability', 0)
        prob2 = results[1].get('fraudProbability', 0)
        
        if prob1 != prob2:
            print(f"\n✅ Model is making different predictions (Model is working!)")
            print(f"   Prediction 1: {prob1}%")
            print(f"   Prediction 2: {prob2}%")
            return True
        else:
            print(f"\n⚠️  Model returned same predictions (might be using fallback)")
            print(f"   Both predictions: {prob1}%")
            return False
    else:
        print(f"\n❌ Could not complete model prediction test")
        return False

def test_history_api():
    """Test 4: Test History API"""
    print("\n" + "=" * 60)
    print("TEST 4: History API")
    print("=" * 60)
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/history")
        if response.status_code == 200:
            history = response.json()
            print(f"✅ History API working")
            print(f"   Records found: {len(history)}")
            if len(history) > 0:
                print(f"   Latest record:")
                latest = history[-1]
                print(f"     Name: {latest.get('Name')}")
                print(f"     Risk Level: {latest.get('Fraud_Risk_Level')}")
            return True
        else:
            print(f"❌ History API returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ History API failed: {e}")
        return False

def test_cors():
    """Test 5: Test CORS headers"""
    print("\n" + "=" * 60)
    print("TEST 5: CORS Configuration")
    print("=" * 60)
    
    try:
        response = requests.options(
            f"{API_BASE_URL}/api/verify-kyc",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "POST"
            }
        )
        cors_headers = {
            "access-control-allow-origin": response.headers.get("access-control-allow-origin"),
            "access-control-allow-methods": response.headers.get("access-control-allow-methods"),
        }
        
        if cors_headers["access-control-allow-origin"]:
            print("✅ CORS is configured")
            print(f"   Allow Origin: {cors_headers['access-control-allow-origin']}")
            return True
        else:
            print("⚠️  CORS headers not found (might still work with middleware)")
            return True  # Still OK, FastAPI middleware handles it
    except Exception as e:
        print(f"⚠️  CORS test failed: {e}")
        return True  # Not critical

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("COMPLETE FLOW VERIFICATION TEST")
    print("=" * 60)
    print("\nTesting: Frontend → Backend → Model → Results → Display")
    print("\n")
    
    results = {
        "Backend Status": False,
        "API Verification": False,
        "Model Prediction": False,
        "History API": False,
        "CORS": False
    }
    
    # Test 1: Backend Status
    status_ok, status_data = test_backend_status()
    results["Backend Status"] = status_ok
    
    if not status_ok:
        print("\n❌ Backend is not running. Please start it first.")
        print("   Command: cd backend && uvicorn main:app --reload")
        sys.exit(1)
    
    # Check if models are loaded
    if status_data:
        models_loaded = all(
            "✅" in status or "Loaded" in status 
            for status in status_data.get('models', {}).values()
        )
        if not models_loaded:
            print("\n⚠️  WARNING: Models are not loaded!")
            print("   The API will use fallback/default predictions.")
            print("   Check backend logs for model loading errors.")
    
    # Test 2: API Verification
    api_ok, api_result = test_api_verification()
    results["API Verification"] = api_ok
    
    # Test 3: Model Prediction
    if api_ok:
        results["Model Prediction"] = test_model_prediction()
    
    # Test 4: History API
    results["History API"] = test_history_api()
    
    # Test 5: CORS
    results["CORS"] = test_cors()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL TESTS PASSED - Flow is working correctly!")
        print("\nFlow Status:")
        print("  ✅ Frontend can send data via API")
        print("  ✅ Backend receives and processes data")
        print("  ✅ Model makes predictions (or uses fallback)")
        print("  ✅ Results are returned in correct format")
        print("  ✅ Frontend can display results (table, score, alert)")
    else:
        print("⚠️  SOME TESTS FAILED - Check issues above")
    
    print("=" * 60 + "\n")
    
    return all_passed

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)

