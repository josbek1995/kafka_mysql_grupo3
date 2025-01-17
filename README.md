# Kafka Docker Services Setup

This project sets up a local Kafka environment using Docker Compose. The services include:
- A Kafka broker (`kafka-1`)
- Kafka UI for cluster monitoring
- Kafka Connect for integration
- A custom `stock-consumer` Python service
- MySQL source connector for Kafka Connect

## Prerequisites

1. [Docker](https://docs.docker.com/get-docker/)
2. [Docker Compose](https://docs.docker.com/compose/)

## Services Overview

### Kafka Broker (`kafka-1`)
- Kafka broker and controller.
- Listens on multiple protocols for internal and external communication.

### Kafka UI (`kafka-ui`)
- Provides a web interface to monitor and manage the Kafka cluster.
- Accessible at `http://localhost:7777`.

### Kafka Connect (`kafka-connect`)
- Used for integrating Kafka with external systems.
- Includes a MySQL source connector for streaming data from a MySQL database.

### Stock Consumer (`stock-consumer`)
- Custom Python service to consume Kafka messages.
- Runs a Python script (`kafka_consumer.py`) located in the `./consumer` directory.

## Setup Instructions

### Step 1: Clone the Repository
Clone the project to your local machine:
bash
git clone <repository-url>
cd <repository-directory>


### Step 2: Start the Services
Use Docker Compose to bring up all services:

### Step 3: Verify the Setup
Kafka Broker: Confirm that the Kafka broker is running and accessible at localhost:29092.
Kafka UI: Visit http://localhost:7777 to view the Kafka cluster.
Kafka Connect: Ensure Kafka Connect is running at http://localhost:8083.

docker-compose up -d


### Step 4: Add MySQL Source Connector
Post the MySQL source connector configuration:

curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d '{
  "name": "mysql-source-connector",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
    "tasks.max": "1",
    "connection.url": "jdbc:mysql://fake-database-grupo3-1.cfqay6u8sikg.us-east-1.rds.amazonaws.com:3306/bd-grupo-3-v3?useSSL=false&allowPublicKeyRetrieval=true",
    "connection.user": "admin",
    "connection.password": "awsrdsgruop3fakerlaboratorio",
    "table.whitelist": "Stock",
    "mode": "timestamp+incrementing",
    "incrementing.column.name": "id_stock",
    "timestamp.column.name": "fecha_actualizacion",
    "topic.prefix": "mysql-",
    "poll.interval.ms": "10000",
    "validate.non.null": "false",
    "driver.class": "com.mysql.cj.jdbc.Driver"
  }
}'


"ADICIONAL": al hacer el primer docker compose el container 'stock-consumer' se caera, luego de agregar el paso 4 se debe volver a lanzar el docker-compose up -d