"""
Global Rate Limiter for Semantic Scholar API
Ensures 1 request per second across ALL users/processes
"""
import time
import os
import fcntl
import json

class GlobalRateLimiter:
    def __init__(self, lock_file="thesis/api_rate_limit.lock"):
        self.lock_file = lock_file
        os.makedirs(os.path.dirname(lock_file), exist_ok=True)
        
    def wait_for_slot(self):
        """
        Wait until it's safe to make an API call.
        Uses file locking to coordinate across multiple processes.
        """
        # Create lock file if it doesn't exist
        if not os.path.exists(self.lock_file):
            with open(self.lock_file, 'w') as f:
                json.dump({"last_call": 0}, f)
        
        # Acquire exclusive lock
        with open(self.lock_file, 'r+') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            
            try:
                # Read last call time
                f.seek(0)
                data = json.load(f)
                last_call = data.get("last_call", 0)
                
                # Calculate wait time
                current_time = time.time()
                time_since_last = current_time - last_call
                
                if time_since_last < 1.0:
                    wait_time = 1.0 - time_since_last
                    print(f"    ⏳ Global rate limit: waiting {wait_time:.2f}s...")
                    time.sleep(wait_time)
                
                # Update last call time
                f.seek(0)
                f.truncate()
                json.dump({"last_call": time.time()}, f)
                
            finally:
                # Release lock
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
