#!/usr/bin/env python3
"""
Simple test script for the streaming Chat-PRD service
"""

import requests
import json
import sys
import time

def test_health(base_url):
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"✅ Health: {response.status_code} - {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_non_streaming_chat(base_url):
    """Test non-streaming chat endpoint"""
    print("\n🔍 Testing non-streaming chat...")
    
    test_conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! Can you help me with a simple product idea?"}
    ]
    
    try:
        response = requests.post(
            f"{base_url}/chat",
            json={"conversation": test_conversation},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Non-streaming chat: {result.get('response', 'No response')[:100]}...")
            return True
        else:
            print(f"❌ Non-streaming chat failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Non-streaming chat error: {e}")
        return False

def test_streaming_chat(base_url):
    """Test streaming chat endpoint"""
    print("\n🔍 Testing streaming chat...")
    
    test_conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me a short story about AI in 3 sentences."}
    ]
    
    try:
        response = requests.post(
            f"{base_url}/chat/stream",
            json={"conversation": test_conversation},
            headers={"Accept": "text/event-stream"},
            stream=True,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Streaming started, receiving chunks...")
            chunks = 0
            for line in response.iter_lines(decode_unicode=True):
                if line.startswith('data: '):
                    data = line[6:]
                    if data == '[DONE]':
                        break
                    try:
                        parsed = json.loads(data)
                        if parsed.get('type') == 'chunk':
                            chunks += 1
                            print(f"   Chunk {chunks}: {parsed.get('content', '')}", end='', flush=True)
                        elif parsed.get('type') == 'complete':
                            print(f"\n✅ Streaming complete: {chunks} chunks received")
                            return True
                    except json.JSONDecodeError:
                        continue
            return True
        else:
            print(f"❌ Streaming failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Streaming error: {e}")
        return False

def main():
    """Main test function"""
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"
    
    print(f"🧪 Testing Chat-PRD Streaming Service at {base_url}")
    print("=" * 60)
    
    # Run tests
    tests_passed = 0
    total_tests = 3
    
    if test_health(base_url):
        tests_passed += 1
    
    if test_non_streaming_chat(base_url):
        tests_passed += 1
    
    if test_streaming_chat(base_url):
        tests_passed += 1
    
    print("\n" + "=" * 60)
    print(f"🎯 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ All tests passed! Service is working correctly.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Check the logs above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 