import json
import time
import requests
from confluent_kafka import Consumer, KafkaError

# URL to send the POST request
POST_URL = "https://utec-arquitecture-streaming-production.up.railway.app/connection"

# Kafka consumer configuration
consumer_config = {
    'bootstrap.servers': 'kafka-1:19092',  # Kafka broker
    'group.id': 'stock-updates-consumer',
    'auto.offset.reset': 'latest'  # Start reading at the end of the topic
}

# Topic name
TOPIC = "mysql-Stock"

def create_consumer():
    """Creates and returns a Kafka consumer instance."""
    return Consumer(consumer_config)

def wait_for_topic(consumer, topic, max_retries=30, wait_time=5):
    """
    Retries until the topic is available.
    - max_retries: Number of times to retry
    - wait_time: Seconds to wait between retries
    """
    retries = 0
    while retries < max_retries:
        metadata = consumer.list_topics(timeout=5.0)
        if topic in metadata.topics:
            print(f"✅ Topic '{topic}' is available. Starting consumption...")
            return True
        print(f"⏳ Waiting for topic '{topic}' to be available... ({retries + 1}/{max_retries})")
        time.sleep(wait_time)
        retries += 1

    print(f"❌ Topic '{topic}' not found after {max_retries} retries. Exiting.")
    return False

def consume_messages():
    """Consumes messages from the Kafka topic and sends HTTP requests."""
    consumer = create_consumer()
    
    # Wait for the topic before subscribing
    if not wait_for_topic(consumer, TOPIC):
        consumer.close()
        return

    consumer.subscribe([TOPIC])
    print(f"📡 Subscribed to topic: {TOPIC}")

    try:
        while True:
            msg = consumer.poll(1.0)  # Poll for messages

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"❌ Consumer error: {msg.error()}")
                    break

            # Process the message
            message_value = msg.value().decode('utf-8')
            print(f"📩 Received message: {message_value}")

            try:
                message_data = json.loads(message_value)
                if "payload" in message_data:
                    message_data = message_data["payload"]

                payload = {
                    "id": str(message_data.get("id_stock")),
                    "stock": message_data.get("stock_actual")
                }
                print(f"📦 Parsed message2: {payload}")
                # Send the POST request
                headers = {"Content-Type": "application/json"}
                
                response = requests.post(POST_URL, json=payload, headers=headers)

                if response.status_code in [200, 201]:  # Created/OK
                    print(f"🔍 Raw API Response: {response.text}")  # Debugging step
                    try:
                        response_data = response.json()
                        print(f"✅ POST request successful: {response_data}")
                    except json.JSONDecodeError:
                        print(f"⚠️ Warning: Received empty or invalid JSON response from API. Status: {response.status_code}")

                else:
                    print(f"❌ POST request failed: {response.status_code}, {response.text}")

            except (json.JSONDecodeError, KeyError) as e:
                print(f"⚠️ Error parsing message or sending POST request: {e}")

    except KeyboardInterrupt:
        print("🔴 Consumer interrupted by user")
    finally:
        consumer.close()

if __name__ == "__main__":
    consume_messages()
