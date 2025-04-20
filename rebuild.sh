#!/bin/bash

echo "🧨 Stopping and removing all Docker services and volumes..."
docker-compose down -v

echo "🧹 Removing dangling Docker images..."
docker image prune -f

echo "♻️ Rebuilding and restarting services..."
./start_services.sh
