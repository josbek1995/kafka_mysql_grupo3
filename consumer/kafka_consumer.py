import json
import requests
from confluent_kafka import Consumer, KafkaError

# URL to send the POST request
POST_URL = "https://utec-arquitecture-streaming-production.up.railway.app/connection"

def consume_messages():
    # Kafka consumer configuration
    consumer_config = {
        'bootstrap.servers': 'kafka-1:19092',  # Replace with your Kafka bootstrap server
        'group.id': 'stock-updates-consumer',
        'auto.offset.reset': 'latest'
    }

    # Create the Kafka consumer
    consumer = Consumer(consumer_config)
    topic = 'mysql-Stock'  # Replace with your Kafka topic

    try:
        # Subscribe to the topic
        consumer.subscribe([topic])
        print(f"Subscribed to topic: {topic}")

        while True:
            # Poll for messages
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Consumer error: {msg.error()}")
                    break

            # Process the message
            message_value = msg.value().decode('utf-8')
            print(f"Received message: {message_value}")

            # Parse the message as JSON
            try:
                message_data = json.loads(message_value)
                payload = {
                    "id": str(message_data.get("id_stock")),
                    "stock": message_data.get("stock_actual")
                }

                # Send the POST request
                response = requests.post(POST_URL, json=payload)
                # 201 status created
                if response.status_code == 201 or response.status_code == 200:
                    print(f"POST request successful: {response.json()}")
                else:
                    print(f"POST request failed: {response.status_code}, {response.text}")

            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error parsing message or sending POST request: {e}")

    except KeyboardInterrupt:
        print("Consumer interrupted by user")
    finally:
        # Close the consumer gracefully
        consumer.close()

if __name__ == "__main__":
    consume_messages()
