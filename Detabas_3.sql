SELECT 
    bt.tag_number,
    p.first_name,
    p.last_name,
    f.flight_number,
    dep.airport_code AS departure_airport,
    arr.airport_code AS arrival_airport,
    bt.weight_kg,
    bt.status,
    bt.check_in_time
FROM baggage_tags bt
JOIN passengers p ON bt.passenger_id = p.passenger_id
JOIN flights f ON bt.flight_id = f.flight_id
JOIN airports dep ON f.departure_airport_id = dep.airport_id
JOIN airports arr ON f.arrival_airport_id = arr.airport_id
WHERE f.flight_number = 'UA2456'
ORDER BY p.last_name, p.first_name;