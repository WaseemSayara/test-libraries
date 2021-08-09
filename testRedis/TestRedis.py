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

    def make_key_value_from_file(self, input_file):
        file = open(input_file, "r")
        lines = file.readlines()
        for line in lines:
            if line is not None:
                key_value = line.split(" ")
                self.connection.set(key_value[0], key_value[1])

    def key_should_exist(self, key):
        exist = self.connection.exists(key)
        if exist == 0:
            print("key does not exist")
            raise redis.connection.RedisError

    def key_should_not_exist(self, key):
        exist = self.connection.exists(key)
        if exist == 1:
            print("key exists")
            raise redis.connection.RedisError
