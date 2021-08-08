import redis


class TestRedis:

    def __init__(self, host="localhost", port="6379"):
        self.connection = redis.Redis(host=host, port=port)

    def connect_to_redis(self, host, port):
        try:
            self.connection = redis.Redis(host=host, port=port)
        except redis.connection.ConnectionError:
            print("Wrong Host IP or Port entered")
            raise

    def list_all_keys(self):
        keys = self.connection.keys()
        for i in range(0, len(keys)):
            keys[i] = keys[i].decode('utf-8')
        return keys

    def get_keys(self, pattern):
        keys = self.connection.keys(pattern)
        for i in range(0, len(keys)):
            keys[i] = keys[i].decode('utf-8')
        return keys

    def delete_key(self, key):
        self.connection.delete(key)

    def clean_database(self):
        self.connection.flushdb()

    def add_key_value(self, key, value):
        self.connection.set(key, value)
