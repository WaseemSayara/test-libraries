from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaProducer, KafkaConsumer, errors


class TestKafka:

    def __init__(self, host="localhost:9092"):
        try:
            self.admin_client = KafkaAdminClient(bootstrap_servers=host, client_id='test')
        except errors.NoBrokersAvailable:
            print("connection failed, you must run the server first")
            raise

    def create_topic(self, topic_name):
        try:
            topic_list = [NewTopic(name=topic_name, num_partitions=1, replication_factor=1)]
            self.admin_client.create_topics(new_topics=topic_list, validate_only=False)
        except errors.TopicAlreadyExistsError:
            print("this topic ( " + str(topic_name) + " ) already exist, try different name")
            raise

    def delete_topic(self, topic_name):
        try:
            topic = []
            if type(topic_name) is not list:
                topic.append(topic_name)
            self.admin_client.delete_topics(topic)
        except errors.UnknownTopicOrPartitionError:
            print("the topic you are trying to delete does not exist")
            raise

    def list_all_topics(self, host="localhost:9092"):
        self.admin_client = KafkaAdminClient(bootstrap_servers=host, client_id='test')
        return self.admin_client.list_topics()

    def topic_should_exist(self, topic):
        available_topics = self.list_all_topics()
        if topic in available_topics:
            return True
        else:
            print("topic ( " + str(topic) + ") doesn't exist")
            raise errors.InvalidTopicError

    def topic_should_not_exist(self, topic):
        available_topics = self.list_all_topics()
        if topic not in available_topics:
            return True
        else:
            print("topic ( " + str(topic) + ") still exists")
            raise errors.TopicAlreadyExistsError

    def send_file_to_kafka_topic(self, topic, input_file, host="localhost:9092"):
        try:
            producer = KafkaProducer(bootstrap_servers=host)
            file = open(input_file, "r")
            value = file.read()
            producer.send(topic, value.encode("utf-8"))
        except FileNotFoundError:
            print("file ("+ str(input_file) + ") is not found")
            raise

    def kafka_consumer(self, topic, output_file, host="localhost:9092"):
        consumer = KafkaConsumer(topic, bootstrap_servers=host, auto_offset_reset='earliest', consumer_timeout_ms=1000)
        file = open(output_file, "w+")
        output = ""
        for message in consumer:
            if message.value is not None:
                output += message.value.decode('utf-8')
            else:
                output += "\n"
        file.write(output)
        file.close()
        consumer.unsubscribe()

    def should_not_be_empty(self, file_name):
        file = open(file_name, 'r')
        content = file.read()
        if len(content) != 0:
            return True
        else:
            print("file is empty")
            raise errors.InvalidTopicError

