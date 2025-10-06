#!/bin/bash

# Base URL
BASE_URL="http://localhost:5000"

echo "=== Testing Travel Document Generator API ==="
echo

# 1. Health Check
echo "1. Health Check:"
curl -s -X GET "$BASE_URL/api/health" | jq .
echo

# 2. Get Airports
echo "2. Get Airports:"
curl -s -X GET "$BASE_URL/api/airports" | jq '.data | length' | xargs echo "Number of airports:"
echo

# 3. Generate Boarding Pass
echo "3. Generate Boarding Pass:"
curl -s -X POST "$BASE_URL/api/generate/boarding-pass" \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "John",
    "lastName": "Doe",
    "pnr": "ABC123",
    "flight": "PH 0121",
    "from": "BOM",
    "fromTerminal": "T1",
    "to": "DEL",
    "toTerminal": "T3",
    "date": "2023-09-10",
    "time": "13:15",
    "arrivalDate": "2023-09-10",
    "arrivalTime": "15:35",
    "boardingTime": "12:45",
    "seat": "14A",
    "class": "Y",
    "sequence": "001A",
    "gate": "B12"
  }' | jq '.success'
echo

# 4. Generate E-Ticket
echo "4. Generate E-Ticket:"
curl -s -X POST "$BASE_URL/api/generate/e-ticket" \
  -H "Content-Type: application/json" \
  -d '{
    "ticketNumber": "0161234567890",
    "pnr": "ABC123",
    "firstName": "John",
    "lastName": "Doe",
    "flight": "PH 0121",
    "from": "BOM",
    "to": "DEL",
    "date": "2023-09-10",
    "time": "13:15",
    "arrivalDate": "2023-09-10",
    "arrivalTime": "15:35"
  }' | jq '.success'
echo

# 5. Generate Baggage Tag
echo "5. Generate Baggage Tag:"
curl -s -X POST "$BASE_URL/api/generate/baggage-tag" \
  -H "Content-Type: application/json" \
  -d '{
    "lastName": "Doe",
    "firstName": "John",
    "pnr": "ABC123",
    "flight": "PH 0121",
    "from": "BOM",
    "to": "DEL",
    "weight": "23",
    "bagNumber": "1234567890"
  }' | jq '.success'
echo

echo "=== API Testing Complete ==="