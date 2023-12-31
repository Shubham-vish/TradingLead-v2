from .redis_cache_factory import RedisCacheFactory

class RedisCacheService:
    def __init__(self):
        self.redis_client = RedisCacheFactory.get_redis_client()

    def set_value(self, key, value):
        self.redis_client.set(key, value)

    def get_value(self, key):
        return self.redis_client.get(key)
    
    def get_decoded_value(self, key):
        value = self.get_value(key)
        if value:
            return value.decode("utf-8")
        else:
            return None
