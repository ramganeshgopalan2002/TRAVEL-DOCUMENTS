-- Create a new booking
CALL CreateNewBooking('Michael', 'Brown', 'michael.brown@example.com', 'UA2456', '24B', 'Y', 21.5);

-- Check in a passenger
CALL CheckInPassenger('ABC123', '15C', 18.0);

-- Get boarding pass details
SELECT * FROM boarding_passes WHERE boarding_pass_id = 1;

-- Find all passengers on a flight
SELECT p.first_name, p.last_name, bp.seat_number, bp.seat_class
FROM boarding_passes bp
JOIN passengers p ON bp.passenger_id = p.passenger_id
JOIN flights f ON bp.flight_id = f.flight_id
WHERE f.flight_number = 'UA2456'
ORDER BY bp.seat_number;