#!/bin/bash

echo "🛠️ Building and starting Docker services..."
docker-compose up --build

echo "✅ Waiting for RabbitMQ to be ready..."
sleep 5

echo "🔌 Enabling MQTT plugin in RabbitMQ..."
docker exec rabbitmq rabbitmq-plugins enable rabbitmq_mqtt

echo "🧪 Sending test message through MQTT..."
sleep 3  # wait for subscriber to fully initialize
python3 ./test/send_test_message.py

echo "✅ Services are running and test message sent."
