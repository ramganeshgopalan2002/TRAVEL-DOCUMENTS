SELECT 
    bp.boarding_pass_id,
    p.first_name,
    p.last_name,
    f.flight_number,
    a.airline_name,
    dep.airport_code AS departure_airport,
    arr.airport_code AS arrival_airport,
    f.departure_date,
    f.departure_time,
    bp.seat_number,
    bp.seat_class,
    bp.gate,
    bp.boarding_time
FROM boarding_passes bp
JOIN passengers p ON bp.passenger_id = p.passenger_id
JOIN flights f ON bp.flight_id = f.flight_id
JOIN airlines a ON f.airline_id = a.airline_id
JOIN airports dep ON f.departure_airport_id = dep.airport_id
JOIN airports arr ON f.arrival_airport_id = arr.airport_id
WHERE f.flight_number = 'UA2456'
ORDER BY bp.seat_number;