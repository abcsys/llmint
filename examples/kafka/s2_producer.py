from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

from s1_register import schema_str_v1

# Producer configuration
config = {
    'bootstrap.servers': 'localhost:9092',
    'key.serializer': StringSerializer('utf_8'),
}

# Schema Registry Client
schema_registry_client = SchemaRegistryClient({'url': 'http://localhost:8081'})
value_serializer = AvroSerializer(schema_registry_client, schema_str_v1)

# Adding the AvroSerializer for value serialization
config['value.serializer'] = value_serializer

# Create producer
producer = SerializingProducer(config)

# User data to be sent
user_data = {"name": "John Doe", "age": 28}

# Produce message
producer.produce(topic='user-info', key=str(user_data['name']), value=user_data)
producer.flush()

print("Message sent successfully with v1 schema!")
