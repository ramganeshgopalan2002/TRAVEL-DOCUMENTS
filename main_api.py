cat > main.py << 'EOF'
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Boarding Pass API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Passenger(BaseModel):
    id: Optional[int] = None
    name: str
    flight_number: str
    seat: str
    boarding_time: str

passengers_db = []
current_id = 1

@app.get("/")
async def root():
    return {"message": "Boarding Pass API is running"}

@app.get("/passengers")
async def get_passengers():
    return passengers_db

@app.post("/passengers")
async def create_passenger(passenger: Passenger):
    global current_id
    passenger.id = current_id
    current_id += 1
    passengers_db.append(passenger)
    return passenger

@app.get("/passengers/{passenger_id}")
async def get_passenger(passenger_id: int):
    passenger = next((p for p in passengers_db if p.id == passenger_id), None)
    if not passenger:
        raise HTTPException(status_code=404, detail="Passenger not found")
    return passenger
EOF