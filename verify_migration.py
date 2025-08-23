#!/usr/bin/env python3
"""
Verification script for Awesome ChatGPT Prompts - Python Edition
Tests all key functionality to ensure the migration was successful
"""

import requests
import json
import time
from pathlib import Path

def print_header():
    """Print verification header"""
    print("🔍 Awesome ChatGPT Prompts - Python Migration Verification")
    print("=" * 60)
    print()

def test_flask_server():
    """Test if Flask development server is running"""
    print("🌐 Testing Flask Development Server...")
    
    try:
        # Test main page
        response = requests.get("http://localhost:4001/", timeout=5)
        if response.status_code == 200:
            print("✅ Main page accessible")
            if "Awesome ChatGPT Prompts" in response.text:
                print("✅ Page content correct")
            else:
                print("❌ Page content incorrect")
        else:
            print(f"❌ Main page returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Flask server not accessible: {e}")
        print("💡 Start Flask server with: python app.py")
        return False
    
    return True

def test_api_endpoints():
    """Test all API endpoints"""
    print("\n🔌 Testing API Endpoints...")
    
    endpoints = [
        ("/api/prompts", "Prompts API"),
        ("/api/prompts?audience=developers", "Developer Prompts API"),
        ("/api/search?q=python", "Search API"),
        ("/api/github-stars", "GitHub Stars API"),
    ]
    
    all_working = True
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"http://localhost:4001{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {name} working")
                # Test JSON response
                try:
                    data = response.json()
                    print(f"   📊 Response: {len(data)} items")
                except json.JSONDecodeError:
                    print(f"   ⚠️  Response not valid JSON")
            else:
                print(f"❌ {name} returned status {response.status_code}")
                all_working = False
        except requests.exceptions.RequestException as e:
            print(f"❌ {name} failed: {e}")
            all_working = False
    
    return all_working

def test_static_generation():
    """Test static site generation"""
    print("\n🏗️  Testing Static Site Generation...")
    
    try:
        # Clean and rebuild
        import subprocess
        result = subprocess.run(["python", "build.py", "build"], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Static site built successfully")
            
            # Check if files were generated
            build_dir = Path("_site")
            if build_dir.exists():
                files = list(build_dir.glob("*"))
                print(f"   📁 Generated {len(files)} files")
                
                # Check key files
                key_files = ["index.html", "style.css", "script.js", "prompts.csv"]
                for file_name in key_files:
                    if (build_dir / file_name).exists():
                        print(f"   ✅ {file_name} present")
                    else:
                        print(f"   ❌ {file_name} missing")
                        return False
                
                return True
            else:
                print("❌ Build directory not created")
                return False
        else:
            print(f"❌ Build failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Build test failed: {e}")
        return False

def test_static_serving():
    """Test static site serving"""
    print("\n🌐 Testing Static Site Serving...")
    
    try:
        # Start static server
        import subprocess
        import time
        
        # Start server in background
        server_process = subprocess.Popen(["python", "build.py", "serve"], 
                                        stdout=subprocess.DEVNULL, 
                                        stderr=subprocess.DEVNULL)
        
        # Wait for server to start
        time.sleep(3)
        
        # Test static site
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Static site accessible")
            if "Awesome ChatGPT Prompts" in response.text:
                print("✅ Static content correct")
            else:
                print("❌ Static content incorrect")
            
            # Stop server
            server_process.terminate()
            server_process.wait()
            
            return True
        else:
            print(f"❌ Static site returned status {response.status_code}")
            server_process.terminate()
            return False
            
    except Exception as e:
        print(f"❌ Static serving test failed: {e}")
        return False

def test_makefile():
    """Test Makefile functionality"""
    print("\n🔧 Testing Makefile Commands...")
    
    try:
        import subprocess
        
        # Test help command
        result = subprocess.run(["make", "help"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and "Available commands:" in result.stdout:
            print("✅ Makefile help working")
        else:
            print("❌ Makefile help failed")
            return False
        
        # Test clean command
        result = subprocess.run(["make", "clean"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Makefile clean working")
        else:
            print("❌ Makefile clean failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Makefile test failed: {e}")
        return False

def test_data_integrity():
    """Test that all data is preserved"""
    print("\n📊 Testing Data Integrity...")
    
    try:
        # Check CSV files
        csv_files = ["prompts.csv", "vibeprompts.csv"]
        for csv_file in csv_files:
            if Path(csv_file).exists():
                with open(csv_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if len(lines) > 1:  # Has header + data
                        print(f"✅ {csv_file}: {len(lines)-1} prompts")
                    else:
                        print(f"❌ {csv_file}: No data found")
                        return False
            else:
                print(f"❌ {csv_file} not found")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Data integrity test failed: {e}")
        return False

def main():
    """Main verification function"""
    print_header()
    
    tests = [
        ("Flask Development Server", test_flask_server),
        ("API Endpoints", test_api_endpoints),
        ("Static Site Generation", test_static_generation),
        ("Static Site Serving", test_static_serving),
        ("Makefile Commands", test_makefile),
        ("Data Integrity", test_data_integrity),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "=" * 60)
    print("📋 VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Migration successful!")
        print("\n🚀 Your Python-based system is working perfectly!")
        print("💡 Use 'python app.py' for development")
        print("💡 Use 'make build' for production builds")
    else:
        print(f"⚠️  {total - passed} tests failed. Check the issues above.")
        print("💡 Some functionality may not work correctly.")
    
    return passed == total

if __name__ == '__main__':
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Verification interrupted")
        exit(1)
    except Exception as e:
        print(f"\n❌ Verification failed: {e}")
        exit(1)
