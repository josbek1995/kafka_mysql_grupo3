# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy application files
COPY kafka_consumer.py /app/
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV BOOTSTRAP_SERVERS="kafka:9092"
ENV TOPIC_NAME="mysql-Stock"
ENV GROUP_ID="mysql-operations-group"

# Add the Python Kafka Consumer script to the container
COPY kafka_consumer.py /app/kafka_consumer.py

# Run the Python consumer script
CMD ["python", "kafka_consumer.py"]
