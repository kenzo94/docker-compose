from flask import Flask
import redis
import time

app = Flask(__name__)
cache = redis.Redis(host="redis", port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            #cache.reset_retry_count()
            return cache.incr("hits")
        except redis.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)
            
@app.rout("/")
def hello():
    count = get_hit_count()
    return "Hello Hung ! I have been seen {} times.\n".format(count)