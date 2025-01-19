from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

from s3_evolve import schema_str_v2

# Producer configuration
config = {
    'bootstrap.servers': 'localhost:9092',
    'key.serializer': StringSerializer('utf_8'),
}

schema_registry_client = SchemaRegistryClient({'url': 'http://localhost:8081'})
value_serializer = AvroSerializer(schema_registry_client, schema_str_v2)
config['value.serializer'] = value_serializer
producer = SerializingProducer(config)

# Updated user data to be sent with the new schema
user_data = {"name": "Jane Doe", "age": 27, "email": "janedoe@example.com"}
print("User:", user_data)

# Produce message
producer.produce(topic='user-info', key=str(user_data['name']), value=user_data)
producer.flush()

print("Message sent successfully with v2 schema!")
