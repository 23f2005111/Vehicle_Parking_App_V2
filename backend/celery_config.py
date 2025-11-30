broker_url = "redis://localhost:6379/0"  # what part of redis will hit to get or send info
result_backend = "redis://localhost:6379/1"   # all data info going in and out databse
timezone = "Asia/Kolkata"
broker_connection_retry_on_startup = True