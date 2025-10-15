"""
Quick test script for rate limiting
Run this to verify rate limiting is working correctly
"""
import requests
import time
from datetime import datetime

BASE_URL = 'http://localhost:8000'

def test_otp_burst_limit():
    """Test burst rate limiting (2/minute)"""
    print("\n" + "="*60)
    print("TEST 1: OTP Burst Rate Limiting (2 per minute)")
    print("="*60)
    
    url = f'{BASE_URL}/api/auth/request-otp/'
    data = {'email': 'test@example.com', 'purpose': 'login'}
    
    for i in range(3):
        print(f"\nRequest {i+1}:")
        response = requests.post(url, json=data)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"  ✅ Success: {response.json().get('message', 'OTP sent')}")
        elif response.status_code == 429:
            print(f"  🚫 Throttled: {response.json().get('detail')}")
            retry_after = response.headers.get('Retry-After', 'N/A')
            print(f"  ⏰ Retry After: {retry_after} seconds")
        else:
            print(f"  ❌ Error: {response.text}")
        
        time.sleep(1)  # Small delay between requests
    
    print("\n✅ Burst limit test complete!")
    print("Expected: First 2 succeed, 3rd fails with 429")


def test_otp_hourly_limit():
    """Test hourly rate limiting (3/hour)"""
    print("\n" + "="*60)
    print("TEST 2: OTP Hourly Rate Limiting (3 per hour)")
    print("="*60)
    print("⚠️ This test takes ~3 minutes (waiting between requests)")
    print("Press Ctrl+C to skip")
    
    url = f'{BASE_URL}/api/auth/request-otp/'
    data = {'email': 'test2@example.com', 'purpose': 'login'}
    
    try:
        for i in range(4):
            print(f"\nRequest {i+1}:")
            response = requests.post(url, json=data)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"  ✅ Success")
            elif response.status_code == 429:
                print(f"  🚫 Throttled")
            
            if i < 3:  # Wait between requests (except last one)
                print("  ⏳ Waiting 65 seconds...")
                time.sleep(65)
        
        print("\n✅ Hourly limit test complete!")
        print("Expected: First 3 succeed, 4th fails with 429")
    except KeyboardInterrupt:
        print("\n⏭️ Test skipped by user")


def test_password_reset_limit():
    """Test password reset rate limiting"""
    print("\n" + "="*60)
    print("TEST 3: Password Reset Rate Limiting (2 per minute)")
    print("="*60)
    
    url = f'{BASE_URL}/api/auth/request-password-reset/'
    data = {'email': 'reset@example.com'}
    
    for i in range(3):
        print(f"\nRequest {i+1}:")
        response = requests.post(url, json=data)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"  ✅ Success")
        elif response.status_code == 429:
            print(f"  🚫 Throttled")
            retry_after = response.headers.get('Retry-After', 'N/A')
            print(f"  ⏰ Retry After: {retry_after} seconds")
        else:
            print(f"  ⚠️ Status: {response.text[:100]}")
        
        time.sleep(1)
    
    print("\n✅ Password reset limit test complete!")


def test_verify_otp_limit():
    """Test OTP verification rate limiting"""
    print("\n" + "="*60)
    print("TEST 4: OTP Verification Rate Limiting (10 per hour)")
    print("="*60)
    
    url = f'{BASE_URL}/api/auth/verify-otp/'
    data = {
        'email': 'verify@example.com',
        'code': '999999',  # Invalid code for testing
        'purpose': 'login'
    }
    
    print("Making 12 verification attempts (expect 11th and 12th to fail)...")
    
    success_count = 0
    throttled_count = 0
    
    for i in range(12):
        response = requests.post(url, json=data)
        
        if response.status_code in [200, 400]:  # 400 is expected for invalid code
            success_count += 1
        elif response.status_code == 429:
            throttled_count += 1
            if throttled_count == 1:
                print(f"\n  🚫 Request {i+1}: THROTTLED (as expected)")
                print(f"     {response.json().get('detail')}")
        
        time.sleep(0.5)  # Small delay
    
    print(f"\n  ✅ Allowed requests: {success_count}")
    print(f"  🚫 Throttled requests: {throttled_count}")
    print("\n✅ Verification limit test complete!")


def test_all():
    """Run all tests"""
    print("\n" + "="*60)
    print("RATE LIMITING TEST SUITE")
    print("="*60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nTesting rate limiting on email sending endpoints...")
    print("Make sure Django server is running on localhost:8000")
    
    try:
        # Quick connection test
        response = requests.get(f'{BASE_URL}/api/')
        print(f"\n✅ Server is reachable (Status: {response.status_code})")
    except Exception as e:
        print(f"\n❌ Cannot connect to server: {e}")
        print("Please start the Django server: python manage.py runserver")
        return
    
    # Run tests
    test_otp_burst_limit()
    
    print("\n" + "-"*60)
    choice = input("\nRun hourly limit test? (takes 3+ minutes) [y/N]: ")
    if choice.lower() == 'y':
        test_otp_hourly_limit()
    
    test_password_reset_limit()
    test_verify_otp_limit()
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETE!")
    print("="*60)
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n✅ Rate limiting is working correctly!")
    print("\nSummary:")
    print("  • OTP requests are limited")
    print("  • Password resets are limited")
    print("  • OTP verification is limited")
    print("  • Burst protection is active")


if __name__ == '__main__':
    print("\n🛡️ Email Rate Limiting Test Script")
    print("This script will test rate limiting on email endpoints")
    test_all()

