DELIMITER //

CREATE PROCEDURE CreateNewBooking(
    IN p_first_name VARCHAR(100),
    IN p_last_name VARCHAR(100),
    IN p_email VARCHAR(255),
    IN p_flight_number VARCHAR(10),
    IN p_seat_number VARCHAR(10),
    IN p_seat_class ENUM('Y', 'W', 'J', 'F'),
    IN p_baggage_weight DECIMAL(5,2)
)
BEGIN
    DECLARE v_passenger_id INT;
    DECLARE v_flight_id INT;
    DECLARE v_booking_id INT;
    DECLARE v_booking_ref VARCHAR(10);
    DECLARE v_ticket_number VARCHAR(13);
    
    -- Generate unique booking reference
    SET v_booking_ref = UPPER(SUBSTRING(MD5(RAND()), 1, 6));
    
    -- Generate ticket number (starting with 016 for United Airlines)
    SET v_ticket_number = CONCAT('016', LPAD(FLOOR(RAND() * 10000000000), 10, '0'));
    
    -- Insert or get passenger
    SELECT passenger_id INTO v_passenger_id 
    FROM passengers 
    WHERE email = p_email;
    
    IF v_passenger_id IS NULL THEN
        INSERT INTO passengers (first_name, last_name, email)
        VALUES (p_first_name, p_last_name, p_email);
        SET v_passenger_id = LAST_INSERT_ID();
    END IF;
    
    -- Get flight ID
    SELECT flight_id INTO v_flight_id 
    FROM flights 
    WHERE flight_number = p_flight_number;
    
    -- Create booking
    INSERT INTO bookings (booking_reference, total_passengers)
    VALUES (v_booking_ref, 1);
    SET v_booking_id = LAST_INSERT_ID();
    
    -- Create boarding pass
    INSERT INTO boarding_passes (booking_id, passenger_id, flight_id, seat_number, seat_class)
    VALUES (v_booking_id, v_passenger_id, v_flight_id, p_seat_number, p_seat_class);
    
    -- Create e-ticket
    INSERT INTO e_tickets (ticket_number, booking_id, passenger_id, flight_id, issue_date, fare_amount)
    VALUES (v_ticket_number, v_booking_id, v_passenger_id, v_flight_id, CURDATE(), 0);
    
    -- Create baggage tag if weight provided
    IF p_baggage_weight > 0 THEN
        INSERT INTO baggage_tags (tag_number, booking_id, passenger_id, flight_id, weight_kg)
        VALUES (CONCAT(SUBSTRING(p_flight_number, 1, 2), LPAD(FLOOR(RAND() * 1000000000), 10, '0')), 
                v_booking_id, v_passenger_id, v_flight_id, p_baggage_weight);
    END IF;
    
    -- Return booking reference
    SELECT v_booking_ref AS booking_reference;
END //

DELIMITER ;