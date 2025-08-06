import redis
import os

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
client = redis.Redis.from_url(redis_url)