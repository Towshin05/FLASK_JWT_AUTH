#!/bin/bash
echo "Testing API..."

echo "1. Testing base route:"
curl http://127.0.0.1:5000/

echo -e "\n\n2. Testing registration:"
curl -X POST http://127.0.0.1:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "testpass123"}'

echo -e "\n\n3. Testing login:"
curl -X POST http://127.0.0.1:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'