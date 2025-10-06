SELECT 
    CONCAT(
        'M1',
        UPPER(CONCAT(p.last_name, '/', p.first_name)),
        'E',
        'ABC123', -- PNR code (would come from booking system)
        UPPER(CONCAT(dep.airport_code, arr.airport_code)),
        REPLACE(f.flight_number, ' ', ''),
        DATE_FORMAT(f.departure_date, '%j'), -- Julian date
        bp.seat_class,
        bp.seat_number,
        '001A', -- Check-in sequence
        '0001', -- Passenger status
        '0' -- Version number
    ) AS iata_bcbp_data
FROM boarding_passes bp
JOIN passengers p ON bp.passenger_id = p.passenger_id
JOIN flights f ON bp.flight_id = f.flight_id
JOIN airports dep ON f.departure_airport_id = dep.airport_id
JOIN airports arr ON f.arrival_airport_id = arr.airport_id
WHERE bp.boarding_pass_id = 1;