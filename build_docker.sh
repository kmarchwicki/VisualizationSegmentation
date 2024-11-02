#!/bin/bash

cd "$(dirname "$0")"

# Start Redis server
docker-compose -f docker_compose.yml up --build