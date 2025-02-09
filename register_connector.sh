#!/bin/bash

echo "Waiting for Kafka Connect to be available..."
while ! curl -s http://kafka-connect:8083/connectors; do
    echo "Kafka Connect is not ready yet. Retrying in 5 seconds..."
    sleep 5
done

echo "Kafka Connect is ready! Registering MySQL Source Connector..."

curl -X POST http://kafka-connect:8083/connectors -H "Content-Type: application/json" -d '{
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
    "poll.interval.ms": "5000",
    "validate.non.null": "false",
    "driver.class": "com.mysql.cj.jdbc.Driver"
  }
}'

echo "Connector registered successfully!"
