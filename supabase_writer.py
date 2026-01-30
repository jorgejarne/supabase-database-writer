#!/usr/bin/env python3
"""
Supabase Database Writer with Anti-Blocking Measures
Sends continuous WRITE requests to a Supabase endpoint with rate limiting
"""

import requests
import time
import random
import json
from datetime import datetime
from typing import Dict, Any
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
API_KEY = os.getenv('SUPABASE_API_KEY')

class SupabaseWriter:
    def __init__(self, url: str, api_key: str):
        """
        Initialize the Supabase writer
        
        Args:
            url: Supabase REST API endpoint (e.g., https://xxx.supabase.co/rest/v1/submissions)
            api_key: Your Supabase anon key
        """
        self.url = url
        self.headers = {
            "apikey": api_key,
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"  # Return the inserted data
        }
        self.request_count = 0
        self.success_count = 0
        self.error_count = 0
        
    def generate_random_data(self) -> Dict[str, Any]:
        """Generate random submission data"""
        names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry"]
        domains = ["gmail.com", "yahoo.com", "outlook.com", "example.com"]
        messages = [
            "Test submission",
            "Hello from the API",
            "Automated test message",
            "Sample data entry",
            "Testing database writes"
        ]
        
        return {
            "name": random.choice(names),
            "email": f"{random.choice(names).lower()}{random.randint(1, 999)}@{random.choice(domains)}",
            "message": random.choice(messages)
        }
    
    def send_write_request(self, data: Dict[str, Any]) -> bool:
        """
        Send a POST request to insert data
        
        Args:
            data: Dictionary containing the data to insert
            
        Returns:
            True if successful, False otherwise
        """
        try:
            response = requests.post(
                self.url,
                headers=self.headers,
                json=data,
                timeout=10
            )
            
            self.request_count += 1
            
            if response.status_code in [200, 201]:
                self.success_count += 1
                print(f"✓ Request #{self.request_count} - SUCCESS")
                print(f"  Inserted: {data['name']} ({data['email']})")
                return True
            else:
                self.error_count += 1
                print(f"✗ Request #{self.request_count} - FAILED (Status: {response.status_code})")
                print(f"  Response: {response.text[:100]}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.error_count += 1
            print(f"✗ Request #{self.request_count} - ERROR: {str(e)}")
            return False
    
    def print_statistics(self):
        """Print current statistics"""
        print("\n" + "="*60)
        print(f"Statistics at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Requests: {self.request_count}")
        print(f"Successful: {self.success_count}")
        print(f"Failed: {self.error_count}")
        if self.request_count > 0:
            success_rate = (self.success_count / self.request_count) * 100
            print(f"Success Rate: {success_rate:.2f}%")
        print("="*60 + "\n")
    
    def run_infinite_loop(self, 
                         min_delay: float = 1.0,
                         max_delay: float = 3.0,
                         batch_size: int = 10,
                         long_pause_after: int = 50,
                         long_pause_duration: float = 10.0):
        """
        Run infinite loop with anti-blocking measures
        
        Args:
            min_delay: Minimum delay between requests (seconds)
            max_delay: Maximum delay between requests (seconds)
            batch_size: Number of requests before showing statistics
            long_pause_after: Take a longer pause after this many requests
            long_pause_duration: Duration of the long pause (seconds)
        """
        print("Starting Supabase Writer...")
        print(f"Target URL: {self.url}")
        print(f"Delay range: {min_delay}s - {max_delay}s")
        print(f"Long pause every {long_pause_after} requests ({long_pause_duration}s)")
        print("\nPress Ctrl+C to stop\n")
        
        try:
            while True:
                # Generate and send data
                data = self.generate_random_data()
                self.send_write_request(data)
                
                # Show statistics periodically
                if self.request_count % batch_size == 0:
                    self.print_statistics()
                
                # Take a longer pause after certain number of requests
                if self.request_count % long_pause_after == 0:
                    print(f"\n⏸ Taking a {long_pause_duration}s pause to avoid rate limiting...\n")
                    time.sleep(long_pause_duration)
                
                # Random delay between requests (anti-pattern detection)
                delay = random.uniform(min_delay, max_delay)
                time.sleep(delay)
                
        except KeyboardInterrupt:
            print("\n\nStopping...")
            self.print_statistics()
            print("Goodbye!")

def main():
    # Anti-blocking settings (adjust these as needed)
    MIN_DELAY = 2.0          # Minimum 2 seconds between requests
    MAX_DELAY = 5.0          # Maximum 5 seconds between requests
    BATCH_SIZE = 10          # Show stats every 10 requests
    LONG_PAUSE_AFTER = 50    # Take a break after 50 requests
    LONG_PAUSE_DURATION = 15.0  # 15 second break
    
    # Create writer instance
    writer = SupabaseWriter(SUPABASE_URL, API_KEY)
    
    # Start the infinite loop
    writer.run_infinite_loop(
        min_delay=MIN_DELAY,
        max_delay=MAX_DELAY,
        batch_size=BATCH_SIZE,
        long_pause_after=LONG_PAUSE_AFTER,
        long_pause_duration=LONG_PAUSE_DURATION
    )

if __name__ == "__main__":
    main()
