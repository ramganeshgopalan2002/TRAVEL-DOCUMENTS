curl -X POST http://localhost:5000/api/generate/baggage-tag \
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
  }'