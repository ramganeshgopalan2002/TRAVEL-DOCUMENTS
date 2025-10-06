curl -X POST http://localhost:5000/api/generate/boarding-pass \
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
  }'