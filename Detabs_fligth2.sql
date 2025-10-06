SELECT 
    p.first_name,
    p.last_name,
    f.flight_number,
    a.airline_name,
    dep.airport_code AS departure_airport,
    dep.city AS departure_city,
    arr.airport_code AS arrival_airport,
    arr.city AS arrival_city,
    f.departure_date,
    f.departure_time,
    bp.seat_number,
    bp.seat_class,
    et.ticket_number
FROM passengers p
JOIN boarding_passes bp ON p.passenger_id = bp.passenger_id
JOIN flights f ON bp.flight_id = f.flight_id
JOIN airlines a ON f.airline_id = a.airline_id
JOIN airports dep ON f.departure_airport_id = dep.airport_id
JOIN airports arr ON f.arrival_airport_id = arr.airport_id
LEFT JOIN e_tickets et ON p.passenger_id = et.passenger_id AND f.flight_id = et.flight_id
WHERE p.passenger_id = 1
ORDER BY f.departure_date DESC;