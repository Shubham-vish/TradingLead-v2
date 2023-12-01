import redis
from ..KeyVault.keyvault_service import KeyVaultService

class RedisCacheFactory:
    _redis_instance = None

    @staticmethod
    def get_redis_client():
        if RedisCacheFactory._redis_instance is None:
            kv_service = KeyVaultService()
            redis_host = kv_service.get_secret("RedisHost")
            redis_key = kv_service.get_secret("RedisKey")
            RedisCacheFactory._redis_instance = redis.StrictRedis(
                host=redis_host, port=6380, db=0, password=redis_key, ssl=True)
        return RedisCacheFactory._redis_instance
