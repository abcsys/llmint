from confluent_kafka import avro
from confluent_kafka.avro import AvroConsumer

consumer = AvroConsumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'test-group',
    'schema.registry.url': 'http://localhost:8081'
})

consumer.subscribe(['user-info'])

while True:
    msg = consumer.poll(1.0)
    if msg is not None:
        print(msg.value())
    else:
        break

consumer.close()
