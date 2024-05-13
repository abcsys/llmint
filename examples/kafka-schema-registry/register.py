from confluent_kafka.schema_registry import SchemaRegistryClient, Schema

# Configuration for the Schema Registry client
schema_registry_conf = {
    'url': 'http://localhost:8081'  # Update with your Schema Registry URL if different
}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Define the initial schema (v1)
schema_str_v1 = """
{
  "type": "record",
  "name": "User",
  "namespace": "com.example",
  "fields": [
    {"name": "name", "type": "string"},
    {"name": "age", "type": "int"}
  ]
}
"""

# Register schema v1
schema_v1 = Schema(schema_str_v1, schema_type='AVRO')
subject_name = 'user-info-value'
schema_id_v1 = schema_registry_client.register_schema(subject_name, schema_v1)
print("Registered Schema v1 ID:", schema_id_v1)

# Define the evolved schema (v2) with an additional optional field
schema_str_v2 = """
{
  "type": "record",
  "name": "User",
  "namespace": "com.example",
  "fields": [
    {"name": "name", "type": "string"},
    {"name": "age", "type": "int"},
    {"name": "email", "type": ["null", "string"], "default": null}
  ]
}
"""

# Register schema v2
schema_v2 = Schema(schema_str_v2, schema_type='AVRO')
schema_id_v2 = schema_registry_client.register_schema(subject_name, schema_v2)
print("Registered Schema v2 ID:", schema_id_v2)
