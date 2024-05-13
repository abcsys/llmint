from confluent_kafka.schema_registry import SchemaRegistryClient, Schema

# Configuration for Schema Registry Client
schema_registry_url = 'http://localhost:8081'
schema_registry_client = SchemaRegistryClient({'url': schema_registry_url})

# Define the initial Avro schema
schema_str_v1 = '''
{
   "namespace": "com.example",
   "type": "record",
   "name": "User",
   "fields": [
       {"name": "name", "type": "string"},
       {"name": "age", "type": "int"}
   ]
}
'''

# Register the schema
schema = Schema(schema_str_v1, schema_type='AVRO')
subject_name = 'user-info-value'
schema_id_v1 = schema_registry_client.register_schema(subject_name, schema)
print(f"Registered Schema ID v1: {schema_id_v1}")
