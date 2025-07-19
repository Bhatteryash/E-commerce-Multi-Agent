import redis
import json
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from dataclasses import dataclass
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class RedisConfig:
    """Redis configuration settings"""
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    decode_responses: bool = True
    socket_connect_timeout: int = 5
    socket_timeout: int = 5

class ECommerceRedisClient:
    """Redis client for e-commerce multi-agent system"""
    
    def __init__(self, config: Optional[RedisConfig] = None):
        self.config = config or RedisConfig()
        self.client = None
        self._connect()
    
    def _connect(self):
        """Establish connection to Redis"""
        try:
            self.client = redis.Redis(
                host=self.config.host,
                port=self.config.port,
                db=self.config.db,
                password=self.config.password,
                decode_responses=self.config.decode_responses,
                socket_connect_timeout=self.config.socket_connect_timeout,
                socket_timeout=self.config.socket_timeout
            )
            # Test connection
            self.client.ping()
            logger.info(f"✅ Connected to Redis at {self.config.host}:{self.config.port}")
        except redis.ConnectionError as e:
            logger.warning(f"⚠️ Could not connect to Redis: {e}. Running without cache.")
            self.client = None
        except Exception as e:
            logger.error(f"❌ Redis connection error: {e}")
            self.client = None
    
    def is_connected(self) -> bool:
        """Check if Redis is connected"""
        return self.client is not None
    
    # Product search caching
    def cache_product_search(self, query: str, budget: str, category: str, result: Dict[str, Any], ttl: int = 3600):
        """Cache product search results"""
        if not self.is_connected():
            return False
        
        try:
            cache_key = self._generate_search_key(query, budget, category)
            cache_data = {
                "result": result,
                "timestamp": datetime.now().isoformat(),
                "query": query,
                "budget": budget,
                "category": category
            }
            
            self.client.setex(cache_key, ttl, json.dumps(cache_data))
            logger.info(f"📦 Cached search result for: {query}")
            return True
        except Exception as e:
            logger.error(f"❌ Error caching search result: {e}")
            return False
    
    def get_cached_search(self, query: str, budget: str, category: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached product search results"""
        if not self.is_connected():
            return None
        
        try:
            cache_key = self._generate_search_key(query, budget, category)
            cached_data = self.client.get(cache_key)
            
            if cached_data:
                data = json.loads(cached_data)
                logger.info(f"📦 Retrieved cached search for: {query}")
                return data
            return None
        except Exception as e:
            logger.error(f"❌ Error retrieving cached search: {e}")
            return None
    
    def _generate_search_key(self, query: str, budget: str, category: str) -> str:
        """Generate cache key for search results"""
        return f"search:{query.lower().replace(' ', '_')}:{budget}:{category}"
    
    # User session management
    def store_user_session(self, session_id: str, user_data: Dict[str, Any], ttl: int = 86400):
        """Store user session data"""
        if not self.is_connected():
            return False
        
        try:
            session_key = f"session:{session_id}"
            session_data = {
                "user_data": user_data,
                "created_at": datetime.now().isoformat(),
                "last_activity": datetime.now().isoformat()
            }
            
            self.client.setex(session_key, ttl, json.dumps(session_data))
            logger.info(f"👤 Stored session: {session_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Error storing session: {e}")
            return False
    
    def get_user_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve user session data"""
        if not self.is_connected():
            return None
        
        try:
            session_key = f"session:{session_id}"
            session_data = self.client.get(session_key)
            
            if session_data:
                data = json.loads(session_data)
                # Update last activity
                data["last_activity"] = datetime.now().isoformat()
                self.client.setex(session_key, 86400, json.dumps(data))  # Refresh TTL
                logger.info(f"👤 Retrieved session: {session_id}")
                return data
            return None
        except Exception as e:
            logger.error(f"❌ Error retrieving session: {e}")
            return None
    
    # User preferences caching
    def store_user_preferences(self, user_id: str, preferences: Dict[str, Any]):
        """Store user preferences"""
        if not self.is_connected():
            return False
        
        try:
            pref_key = f"preferences:{user_id}"
            pref_data = {
                "preferences": preferences,
                "updated_at": datetime.now().isoformat()
            }
            
            self.client.set(pref_key, json.dumps(pref_data))  # No expiration for preferences
            logger.info(f"⚙️ Stored preferences for user: {user_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Error storing preferences: {e}")
            return False
    
    def get_user_preferences(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve user preferences"""
        if not self.is_connected():
            return None
        
        try:
            pref_key = f"preferences:{user_id}"
            pref_data = self.client.get(pref_key)
            
            if pref_data:
                data = json.loads(pref_data)
                logger.info(f"⚙️ Retrieved preferences for user: {user_id}")
                return data
            return None
        except Exception as e:
            logger.error(f"❌ Error retrieving preferences: {e}")
            return None
    
    # Analytics and metrics
    def increment_search_count(self, query: str):
        """Increment search count for analytics"""
        if not self.is_connected():
            return False
        
        try:
            search_key = f"analytics:search:{query.lower().replace(' ', '_')}"
            self.client.incr(search_key)
            
            # Also increment daily count
            daily_key = f"analytics:daily:{datetime.now().strftime('%Y-%m-%d')}"
            self.client.incr(daily_key)
            return True
        except Exception as e:
            logger.error(f"❌ Error incrementing search count: {e}")
            return False
    
    def get_popular_searches(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get popular search queries"""
        if not self.is_connected():
            return []
        
        try:
            search_keys = self.client.keys("analytics:search:*")
            popular_searches = []
            
            for key in search_keys:
                count = self.client.get(key)
                query = key.replace("analytics:search:", "").replace("_", " ")
                popular_searches.append({
                    "query": query,
                    "count": int(count) if count else 0
                })
            
            # Sort by count and limit results
            popular_searches.sort(key=lambda x: x["count"], reverse=True)
            return popular_searches[:limit]
        except Exception as e:
            logger.error(f"❌ Error getting popular searches: {e}")
            return []
    
    # Utility methods
    def clear_cache(self, pattern: str = None):
        """Clear cache entries"""
        if not self.is_connected():
            return False
        
        try:
            if pattern:
                keys = self.client.keys(pattern)
                if keys:
                    self.client.delete(*keys)
                    logger.info(f"🗑️ Cleared {len(keys)} cache entries matching: {pattern}")
            else:
                self.client.flushdb()
                logger.info("🗑️ Cleared all cache entries")
            return True
        except Exception as e:
            logger.error(f"❌ Error clearing cache: {e}")
            return False
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        if not self.is_connected():
            return {"connected": False}
        
        try:
            info = self.client.info()
            return {
                "connected": True,
                "used_memory": info.get("used_memory_human", "N/A"),
                "connected_clients": info.get("connected_clients", 0),
                "total_commands_processed": info.get("total_commands_processed", 0),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0)
            }
        except Exception as e:
            logger.error(f"❌ Error getting cache stats: {e}")
            return {"connected": False, "error": str(e)}

# Global Redis client instance
_redis_client = None

def get_redis_client() -> ECommerceRedisClient:
    """Get or create Redis client instance"""
    global _redis_client
    if _redis_client is None:
        # Try to get Redis config from environment
        config = RedisConfig(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            db=int(os.getenv("REDIS_DB", "0")),
            password=os.getenv("REDIS_PASSWORD")
        )
        _redis_client = ECommerceRedisClient(config)
    return _redis_client

# Convenience functions
def cache_search_result(query: str, budget: str, category: str, result: Dict[str, Any]) -> bool:
    """Convenience function to cache search results"""
    client = get_redis_client()
    return client.cache_product_search(query, budget, category, result)

def get_cached_search_result(query: str, budget: str, category: str) -> Optional[Dict[str, Any]]:
    """Convenience function to get cached search results"""
    client = get_redis_client()
    return client.get_cached_search(query, budget, category)
