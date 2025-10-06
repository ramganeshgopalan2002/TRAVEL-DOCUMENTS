DELIMITER //

CREATE PROCEDURE CheckInPassenger(
    IN p_booking_reference VARCHAR(10),
    IN p_seat_number VARCHAR(10),
    IN p_baggage_weight DECIMAL(5,2)
)
BEGIN
    DECLARE v_booking_id INT;
    DECLARE v_passenger_id INT;
    DECLARE v_flight_id INT;
    DECLARE v_flight_number VARCHAR(10);
    
    -- Get booking details
    SELECT booking_id, passenger_id, flight_id INTO v_booking_id, v_passenger_id, v_flight_id
    FROM boarding_passes bp
    JOIN bookings b ON bp.booking_id = b.booking_id
    WHERE b.booking_reference = p_booking_reference;
    
    -- Get flight number
    SELECT flight_number INTO v_flight_number
    FROM flights
    WHERE flight_id = v_flight_id;
    
    -- Update boarding pass with seat number
    UPDATE boarding_passes 
    SET seat_number = p_seat_number, 
        updated_at = CURRENT_TIMESTAMP
    WHERE booking_id = v_booking_id;
    
    -- Create or update baggage tag
    IF p_baggage_weight > 0 THEN
        IF EXISTS (SELECT 1 FROM baggage_tags WHERE booking_id = v_booking_id) THEN
            UPDATE baggage_tags 
            SET weight_kg = p_baggage_weight, 
                updated_at = CURRENT_TIMESTAMP
            WHERE booking_id = v_booking_id;
        ELSE
            INSERT INTO baggage_tags (tag_number, booking_id, passenger_id, flight_id, weight_kg)
            VALUES (CONCAT(SUBSTRING(v_flight_number, 1, 2), LPAD(FLOOR(RAND() * 1000000000), 10, '0')), 
                    v_booking_id, v_passenger_id, v_flight_id, p_baggage_weight);
        END IF;
    END IF;
    
    -- Log the action
    INSERT INTO document_history (document_type, document_id, action, action_details, performed_by)
    VALUES ('boarding_pass', (SELECT boarding_pass_id FROM boarding_passes WHERE booking_id = v_booking_id), 
            'updated', CONCAT('Check-in completed. Seat: ', p_seat_number, ', Baggage: ', p_baggage_weight, 'kg'), 
            'check_in_system');
    
    SELECT 'Check-in completed successfully' AS message;
END //

DELIMITER ;