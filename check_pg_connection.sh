#!/bin/bash

# Check if PostgreSQL container is up and running
if docker-compose ps | grep -q 'postgres_1.*Up'; then
    echo "PostgreSQL container is up."

    # Attempt to connect to the PostgreSQL database
    docker exec -it postgres psql -U postgres -d flask_jwt_auth -c "SELECT 1" &>/dev/null

    # Check if the connection was successful
    if [ $? -eq 0 ]; then
        echo "Successfully connected to the PostgreSQL database!"
    else
        echo "Failed to connect to the PostgreSQL database."
    fi
else
    echo "PostgreSQL container is not running."
fi
