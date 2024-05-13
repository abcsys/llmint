from confluent_kafka.schema_registry import SchemaRegistryClient, Schema
from s1_register import subject_name

# Configuration for Schema Registry Client
schema_registry_url = 'http://localhost:8081'
schema_registry_client = SchemaRegistryClient({'url': schema_registry_url})

# Define the evolved Avro schema
schema_str_v2 = '''
{
   "namespace": "com.example",
   "type": "record",
   "name": "User",
   "fields": [
       {"name": "name", "type": "string"},
       {"name": "age", "type": "int"},
       {"name": "email", "type": ["null", "string"], "default": null}
   ]
}
'''

# Register the evolved schema
schema = Schema(schema_str_v2, schema_type='AVRO')
schema_id_v2 = schema_registry_client.register_schema(subject_name, schema)
print(f"Registered Schema ID v2: {schema_id_v2}")
