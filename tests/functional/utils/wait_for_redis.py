import time

from redis.client import Redis

if __name__ == '__main__':
    redis_client = Redis(host='redis', port='6379')
    while True:
        if redis_client.ping():
            break
        time.sleep(1)
