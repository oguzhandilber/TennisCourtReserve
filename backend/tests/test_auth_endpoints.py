import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

# Helper to print test results
def print_test_result(test_name, success, response_data=None, error_message=None):
    status = "PASSED" if success else "FAILED"
    print(f"Test: {test_name} - {status}")
    if response_data:
        try:
            print(f"  Response: {json.dumps(response_data, indent=2)}")
        except TypeError:
            print(f"  Response: {response_data}") # In case it's not JSON serializable directly
    if error_message:
        print(f"  Error: {error_message}")
    print("---")

# Test data
new_user_email = f"testplayer_{int(time.time())}@example.com"
new_user_password = "testpassword123"
registered_user_token = None
registered_user_refresh_token = None

def test_user_registration():
    print("Starting test_user_registration...")
    url = f"{BASE_URL}/auth/register"
    payload = {
        "email": new_user_email,
        "password": new_user_password,
        "full_name": "Test Player Registration"
    }
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        if response.status_code == 201 and "message" in data and "user" in data:
            print_test_result("User Registration (Success)", True, data)
            return True
        else:
            print_test_result("User Registration (Success)", False, data, f"Status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_test_result("User Registration (Success)", False, error_message=str(e))
        return False

def test_user_login_correct_credentials():
    print("Starting test_user_login_correct_credentials...")
    global registered_user_token, registered_user_refresh_token
    url = f"{BASE_URL}/auth/login"
    payload = {
        "email": new_user_email,
        "password": new_user_password
    }
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        if response.status_code == 200 and "access_token" in data and "refresh_token" in data:
            registered_user_token = data["access_token"]
            registered_user_refresh_token = data["refresh_token"]
            print_test_result("User Login (Correct Credentials)", True, {"access_token_type": type(data['access_token']).__name__, "refresh_token_type": type(data['refresh_token']).__name__})
            return True
        else:
            print_test_result("User Login (Correct Credentials)", False, data, f"Status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_test_result("User Login (Correct Credentials)", False, error_message=str(e))
        return False

def test_user_login_incorrect_credentials():
    print("Starting test_user_login_incorrect_credentials...")
    url = f"{BASE_URL}/auth/login"
    payload = {
        "email": new_user_email,
        "password": "wrongpassword"
    }
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        if response.status_code == 401:
            print_test_result("User Login (Incorrect Credentials)", True, data)
            return True
        else:
            print_test_result("User Login (Incorrect Credentials)", False, data, f"Status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_test_result("User Login (Incorrect Credentials)", False, error_message=str(e))
        return False

def test_token_refresh():
    print("Starting test_token_refresh...")
    global registered_user_token # Use the new token for subsequent requests if needed
    if not registered_user_refresh_token:
        print_test_result("Token Refresh", False, error_message="Cannot run test: refresh token not available from login.")
        return False
    url = f"{BASE_URL}/auth/refresh"
    headers = {
        "Authorization": f"Bearer {registered_user_refresh_token}"
    }
    try:
        response = requests.post(url, headers=headers)
        data = response.json()
        if response.status_code == 200 and "access_token" in data:
            registered_user_token = data["access_token"] # Update the access token
            print_test_result("Token Refresh", True, {"new_access_token_type": type(data['access_token']).__name__})
            return True
        else:
            print_test_result("Token Refresh", False, data, f"Status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_test_result("Token Refresh", False, error_message=str(e))
        return False

if __name__ == "__main__":
    print("Running Authentication Endpoint Tests...")
    # Wait for server to start if running concurrently
    # time.sleep(5) 

    registration_ok = test_user_registration()
    login_correct_ok = False
    login_incorrect_ok = False
    refresh_ok = False

    if registration_ok:
        login_correct_ok = test_user_login_correct_credentials()
        login_incorrect_ok = test_user_login_incorrect_credentials()
    
    if login_correct_ok:
        refresh_ok = test_token_refresh()

    print("\nAuthentication Endpoint Test Summary:")
    print(f"User Registration: {'PASSED' if registration_ok else 'FAILED'}")
    print(f"User Login (Correct): {'PASSED' if login_correct_ok else 'FAILED'}")
    print(f"User Login (Incorrect): {'PASSED' if login_incorrect_ok else 'FAILED'}")
    print(f"Token Refresh: {'PASSED' if refresh_ok else 'FAILED'}")

    all_passed = registration_ok and login_correct_ok and login_incorrect_ok and refresh_ok
    print(f"\nOverall Auth Test Status: {'PASSED' if all_passed else 'FAILED'}")

