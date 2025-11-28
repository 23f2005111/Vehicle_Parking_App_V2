from flask_caching import Cache


cache = Cache()

def init_cache(app):
    app.config['CACHE_TYPE'] = 'RedisCache'  # connect to redis server for storing info
    app.config['CACHE_REDIS_HOST'] = 'localhost'
    app.config['CACHE_REDIS_PORT'] = 6379
    app.config['CACHE_REDIS_DB'] = 1   # redis database number (DB 1 for cache, DB 0 is used by Celery)
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # default
    
    # connect cache object to Flask app with above configuration
    cache.init_app(app)

    print("Cache initialized with Redis on localhost:6379")
    return cache