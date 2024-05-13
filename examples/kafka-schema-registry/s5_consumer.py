from confluent_kafka import DeserializingConsumer
from confluent_kafka.serialization import StringDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer

# Consumer configuration
consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'user-info-group',
    'auto.offset.reset': 'earliest',
    'key.deserializer': StringDeserializer('utf_8'),
}

schema_registry_client = SchemaRegistryClient({'url': 'http://localhost:8081'})
# Setup AvroDeserializer for consuming
value_deserializer = AvroDeserializer(schema_registry_client)
consumer_config['value.deserializer'] = value_deserializer

# Initialize Consumer
consumer = DeserializingConsumer(consumer_config)
consumer.subscribe(['user-info'])

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
        else:
            print(f"Received message: {msg.value()} with key {msg.key()}")
except KeyboardInterrupt:
    print("Message consumption stopped by user.")
finally:
    consumer.close()

