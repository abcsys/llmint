from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

value_schema = avro.load('user_v1.avsc')
value = {"name": "John Doe", "age": 28}

producer = AvroProducer({
    'bootstrap.servers': 'localhost:9092',
    'schema.registry.url': 'http://localhost:8081'
    }, default_value_schema=value_schema)

producer.produce(topic='user-info', value=value)
producer.flush()