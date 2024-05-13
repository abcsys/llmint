# Setup

In /kafka:

Run zookeeper:

```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
```

Run kafka:

```bash
bin/kafka-server-start.sh config/server.properties
```

In /confluent:

Run schema registry:

```bash
bin/schema-registry-start etc/schema-registry/schema-registry.properties
```

