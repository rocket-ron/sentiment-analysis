from kafka import KafkaProducer
import json


"""

    Simple unbuffered Kafka Producer

"""

class KafkaTweetSerializer:

    _producer = None

    def __init__(self, host='localhost', port='9092'):
        kafka_server = "{0}:{1}".format(host, str(port))
        self._producer = KafkaProducer(bootstrap_servers=[kafka_server],
                                       value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    def write(self, message):
        self._producer.send(topic='tweets', value=message)
        self._producer.flush()
        print "Tweet!"

    def end(self):
        self._producer.close()
