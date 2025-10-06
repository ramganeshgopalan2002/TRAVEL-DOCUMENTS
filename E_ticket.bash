curl -X POST http://localhost:5000/api/generate/e-ticket \
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
  }'