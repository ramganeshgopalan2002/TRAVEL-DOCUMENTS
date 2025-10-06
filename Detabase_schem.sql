-- Create Database
CREATE DATABASE IF NOT EXISTS iata_travel_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE iata_travel_db;

-- Table for Airlines
CREATE TABLE airlines (
    airline_id INT AUTO_INCREMENT PRIMARY KEY,
    airline_code VARCHAR(2) NOT NULL UNIQUE,
    airline_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table for Airports
CREATE TABLE airports (
    airport_id INT AUTO_INCREMENT PRIMARY KEY,
    airport_code VARCHAR(3) NOT NULL UNIQUE,
    airport_name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table for Passengers
CREATE TABLE passengers (
    passenger_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    date_of_birth DATE,
    nationality VARCHAR(100),
    passport_number VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_passenger_name (first_name, last_name),
    INDEX idx_passport (passport_number)
);

-- Table for Flights
CREATE TABLE flights (
    flight_id INT AUTO_INCREMENT PRIMARY KEY,
    flight_number VARCHAR(10) NOT NULL,
    airline_id INT NOT NULL,
    departure_airport_id INT NOT NULL,
    arrival_airport_id INT NOT NULL,
    departure_date DATE NOT NULL,
    departure_time TIME NOT NULL,
    arrival_date DATE NOT NULL,
    arrival_time TIME NOT NULL,
    aircraft_type VARCHAR(50),
    duration_minutes INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (airline_id) REFERENCES airlines(airline_id),
    FOREIGN KEY (departure_airport_id) REFERENCES airports(airport_id),
    FOREIGN KEY (arrival_airport_id) REFERENCES airports(airport_id),
    INDEX idx_flight_number (flight_number),
    INDEX idx_departure_date (departure_date)
);

-- Table for Bookings
CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_reference VARCHAR(10) NOT NULL UNIQUE,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_passengers INT NOT NULL DEFAULT 1,
    booking_status ENUM('confirmed', 'cancelled', 'completed') DEFAULT 'confirmed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_booking_ref (booking_reference)
);

-- Table for Boarding Passes
CREATE TABLE boarding_passes (
    boarding_pass_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    passenger_id INT NOT NULL,
    flight_id INT NOT NULL,
    seat_number VARCHAR(10) NOT NULL,
    seat_class ENUM('Y', 'W', 'J', 'F') NOT NULL,
    boarding_group VARCHAR(5),
    boarding_time TIME,
    gate VARCHAR(10),
    sequence_number INT,
    iata_bcbp_data TEXT,
    qr_code_path VARCHAR(255),
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('issued', 'used', 'cancelled') DEFAULT 'issued',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id),
    FOREIGN KEY (passenger_id) REFERENCES passengers(passenger_id),
    FOREIGN KEY (flight_id) REFERENCES flights(flight_id),
    UNIQUE KEY unique_boarding_pass (flight_id, passenger_id),
    INDEX idx_boarding_pass (boarding_pass_id, passenger_id, flight_id)
);

-- Table for E-Tickets
CREATE TABLE e_tickets (
    ticket_id INT AUTO_INCREMENT PRIMARY KEY,
    ticket_number VARCHAR(13) NOT NULL UNIQUE,
    booking_id INT NOT NULL,
    passenger_id INT NOT NULL,
    flight_id INT NOT NULL,
    issue_date DATE NOT NULL,
    fare_amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    ticket_status ENUM('issued', 'used', 'refunded', 'void') DEFAULT 'issued',
    iata_data TEXT,
    qr_code_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id),
    FOREIGN KEY (passenger_id) REFERENCES passengers(passenger_id),
    FOREIGN KEY (flight_id) REFERENCES flights(flight_id),
    INDEX idx_ticket_number (ticket_number)
);

-- Table for Baggage Tags
CREATE TABLE baggage_tags (
    baggage_id INT AUTO_INCREMENT PRIMARY KEY,
    tag_number VARCHAR(15) NOT NULL UNIQUE,
    booking_id INT NOT NULL,
    passenger_id INT NOT NULL,
    flight_id INT NOT NULL,
    weight_kg DECIMAL(5, 2) NOT NULL,
    check_in_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    barcode_data TEXT,
    barcode_path VARCHAR(255),
    status ENUM('checked', 'loaded', 'transferred', 'delivered', 'lost') DEFAULT 'checked',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id),
    FOREIGN KEY (passenger_id) REFERENCES passengers(passenger_id),
    FOREIGN KEY (flight_id) REFERENCES flights(flight_id),
    INDEX idx_tag_number (tag_number)
);

-- Table for Document History (Audit Log)
CREATE TABLE document_history (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    document_type ENUM('boarding_pass', 'e_ticket', 'baggage_tag') NOT NULL,
    document_id INT NOT NULL,
    action ENUM('created', 'updated', 'cancelled', 'used') NOT NULL,
    action_details TEXT,
    performed_by VARCHAR(100),
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_document_history (document_type, document_id, performed_at)
);

-- Insert sample data for Airlines
INSERT INTO airlines (airline_code, airline_name) VALUES
('UA', 'United Airlines'),
('AA', 'American Airlines'),
('DL', 'Delta Air Lines'),
('LH', 'Lufthansa'),
('BA', 'British Airways'),
('AF', 'Air France'),
('EK', 'Emirates'),
('SQ', 'Singapore Airlines');

-- Insert sample data for Airports
INSERT INTO airports (airport_code, airport_name, city, country) VALUES
('JFK', 'John F. Kennedy International Airport', 'New York', 'United States'),
('LAX', 'Los Angeles International Airport', 'Los Angeles', 'United States'),
('LHR', 'Heathrow Airport', 'London', 'United Kingdom'),
('CDG', 'Charles de Gaulle Airport', 'Paris', 'France'),
('DXB', 'Dubai International Airport', 'Dubai', 'United Arab Emirates'),
('SIN', 'Singapore Changi Airport', 'Singapore', 'Singapore'),
('FRA', 'Frankfurt Airport', 'Frankfurt', 'Germany'),
('ORD', 'O''Hare International Airport', 'Chicago', 'United States'),
('HND', 'Haneda Airport', 'Tokyo', 'Japan'),
('SYD', 'Sydney Airport', 'Sydney', 'Australia');

-- Insert sample data for Passengers
INSERT INTO passengers (first_name, last_name, email, phone, date_of_birth, nationality, passport_number) VALUES
('John', 'Doe', 'john.doe@example.com', '+1-555-0101', '1985-03-15', 'American', 'P1234567'),
('Jane', 'Smith', 'jane.smith@example.com', '+1-555-0102', '1990-07-22', 'British', 'P7654321'),
('Robert', 'Johnson', 'robert.j@example.com', '+1-555-0103', '1978-11-30', 'Canadian', 'P9876543'),
('Maria', 'Garcia', 'maria.g@example.com', '+34-555-0104', '1982-05-14', 'Spanish', 'P4567890'),
('Chen', 'Wei', 'chen.wei@example.com', '+86-555-0105', '1992-09-08', 'Chinese', 'P2468135');

-- Insert sample data for Flights
INSERT INTO flights (flight_number, airline_id, departure_airport_id, arrival_airport_id, departure_date, departure_time, arrival_date, arrival_time, aircraft_type, duration_minutes) VALUES
('UA2456', 1, 1, 3, '2023-07-15', '14:30:00', '2023-07-16', '06:45:00', 'Boeing 777', 855),
('AA1234', 2, 2, 4, '2023-07-16', '10:15:00', '2023-07-17', '08:30:00', 'Airbus A330', 855),
('DL5678', 3, 1, 8, '2023-07-17', '16:45:00', '2023-07-17', '19:20:00', 'Boeing 737', 155),
('LH9012', 4, 7, 5, '2023-07-18', '09:30:00', '2023-07-18', '16:45:00', 'Airbus A380', 315),
('BA3456', 5, 3, 9, '2023-07-19', '13:20:00', '2023-07-20', '09:40:00', 'Boeing 787', 800);

-- Insert sample data for Bookings
INSERT INTO bookings (booking_reference, booking_date, total_passengers, booking_status) VALUES
('ABC123', '2023-06-01 10:30:00', 1, 'confirmed'),
('DEF456', '2023-06-05 14:45:00', 2, 'confirmed'),
('GHI789', '2023-06-10 09:15:00', 1, 'completed'),
('JKL012', '2023-06-15 16:20:00', 3, 'confirmed'),
('MNO345', '2023-06-20 11:05:00', 1, 'cancelled');

-- Insert sample data for Boarding Passes
INSERT INTO boarding_passes (booking_id, passenger_id, flight_id, seat_number, seat_class, boarding_group, boarding_time, gate, sequence_number, iata_bcbp_data, status) VALUES
(1, 1, 1, '23A', 'Y', '3', '13:45:00', 'B12', 42, 'M1DOE/JOHN E ABC123 JFKLHR UA2456 196 Y 23A 001A 0001 0', 'issued'),
(2, 2, 2, '15B', 'W', '2', '09:30:00', 'A5', 28, 'M1SMITH/JANE E DEF456 LAXCDG AA1234 197 W 15B 001A 0001 0', 'issued'),
(3, 3, 3, '8C', 'J', '1', '15:30:00', 'C8', 12, 'M1JOHNSON/ROBERT E GHI789 JFKORD DL5678 198 J 8C 001A 0001 0', 'used'),
(4, 4, 4, '2A', 'F', '1', '08:15:00', 'D3', 5, 'M1GARCIA/MARIA E JKL012 FRADXB LH9012 199 F 2A 001A 0001 0', 'issued');

-- Insert sample data for E-Tickets
INSERT INTO e_tickets (ticket_number, booking_id, passenger_id, flight_id, issue_date, fare_amount, currency, ticket_status, iata_data) VALUES
('0161234567890', 1, 1, 1, '2023-06-01', 850.00, 'USD', 'issued', '0161234567890|DOE/JOHN|UA2456|JFKLHR|230715'),
('0161234567891', 2, 2, 2, '2023-06-05', 1250.00, 'USD', 'issued', '0161234567891|SMITH/JANE|AA1234|LAXCDG|230716'),
('0161234567892', 3, 3, 3, '2023-06-10', 450.00, 'USD', 'used', '0161234567892|JOHNSON/ROBERT|DL5678|JFKORD|230717'),
('0161234567893', 4, 4, 4, '2023-06-15', 2200.00, 'USD', 'issued', '0161234567893|GARCIA/MARIA|LH9012|FRADXB|230718');

-- Insert sample data for Baggage Tags
INSERT INTO baggage_tags (tag_number, booking_id, passenger_id, flight_id, weight_kg, status, barcode_data) VALUES
('UA1234567890', 1, 1, 1, 23.5, 'loaded', 'UA1234567890|DOE/JOHN|UA2456|JFKLHR'),
('AA9876543210', 2, 2, 2, 18.0, 'checked', 'AA9876543210|SMITH/JANE|AA1234|LAXCDG'),
('DL4567890123', 3, 3, 3, 15.5, 'delivered', 'DL4567890123|JOHNSON/ROBERT|DL5678|JFKORD'),
('LH7890123456', 4, 4, 4, 32.0, 'transferred', 'LH7890123456|GARCIA/MARIA|LH9012|FRADXB');

-- Insert sample data for Document History
INSERT INTO document_history (document_type, document_id, action, action_details, performed_by) VALUES
('boarding_pass', 1, 'created', 'Boarding pass issued for John Doe', 'system'),
('e_ticket', 1, 'created', 'E-ticket issued for John Doe', 'system'),
('baggage_tag', 1, 'created', 'Baggage tag created for John Doe', 'system'),
('boarding_pass', 3, 'used', 'Boarding pass scanned at gate', 'gate_agent_12'),
('baggage_tag', 3, 'delivered', 'Baggage delivered to passenger', 'baggage_handler_5');