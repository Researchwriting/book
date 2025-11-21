"""
Paper Cache for Semantic Scholar API
Caches search results to avoid redundant API calls
"""
import json
import os
import hashlib
from datetime import datetime, timedelta

class PaperCache:
    def __init__(self, cache_file="thesis/paper_cache.json", cache_days=7):
        self.cache_file = cache_file
        self.cache_days = cache_days
        self.cache = self._load_cache()
        
    def _load_cache(self):
        """Load cache from file"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading cache: {e}")
                return {}
        return {}
    
    def _save_cache(self):
        """Save cache to file"""
        try:
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def _get_cache_key(self, query, limit):
        """Generate cache key from query"""
        key_string = f"{query}_{limit}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, query, limit=5):
        """Get cached results if available and fresh"""
        cache_key = self._get_cache_key(query, limit)
        
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            cached_time = datetime.fromisoformat(cached_data['timestamp'])
            
            # Check if cache is still fresh
            if datetime.now() - cached_time < timedelta(days=self.cache_days):
                print(f"    💾 Using cached results for: {query[:50]}...")
                return cached_data['results']
        
        return None
    
    def set(self, query, limit, results):
        """Cache search results"""
        cache_key = self._get_cache_key(query, limit)
        self.cache[cache_key] = {
            'query': query,
            'limit': limit,
            'results': results,
            'timestamp': datetime.now().isoformat()
        }
        self._save_cache()
    
    def clear_old_entries(self):
        """Remove cache entries older than cache_days"""
        cutoff = datetime.now() - timedelta(days=self.cache_days)
        keys_to_remove = []
        
        for key, data in self.cache.items():
            cached_time = datetime.fromisoformat(data['timestamp'])
            if cached_time < cutoff:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self.cache[key]
        
        if keys_to_remove:
            self._save_cache()
            print(f"    🗑️  Cleared {len(keys_to_remove)} old cache entries")
