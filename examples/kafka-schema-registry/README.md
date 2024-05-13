# Installation

## Kafka

Download Kafka from [here](https://kafka.apache.org/downloads).

## Confluent

Download Confluent from [here](https://www.confluent.io/download/).

## Confluent python client

Install the confluent python client:

```bash
pip install confluent_kafka
```

```bash

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

