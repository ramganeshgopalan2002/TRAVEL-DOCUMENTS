<?php
require_once 'config.php';

// Only handle POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    sendError('Method not allowed', 405);
}

$data = getJsonInput();

// Validate required fields
$requiredFields = ['firstName', 'lastName', 'flight', 'from', 'to', 'date', 'time', 'seat', 'class'];
foreach ($requiredFields as $field) {
    if (!isset($data[$field]) || empty($data[$field])) {
        sendError("Missing required field: $field");
    }
}

// Validate airport codes
if (strlen($data['from']) !== 3 || strlen($data['to']) !== 3) {
    sendError('Airport codes must be 3 letters');
}

// Parse date
try {
    $flightDate = new DateTime($data['date']);
} catch (Exception $e) {
    sendError('Invalid date format. Use YYYY-MM-DD');
}

// Generate IATA data string
function formatBoardingPassData($firstName, $lastName, $flight, $from, $to, $date, $seat, $classCode) {
    // Format the date in Julian format (DDD) for IATA
    $start = new DateTime($date->format('Y') . '-01-01');
    $diff = $date->diff($start);
    $dayOfYear = $diff->days + 1;
    $julianDate = str_pad($dayOfYear, 3, '0', STR_PAD_LEFT);
    
    // Format the year (YY)
    $year = $date->format('y');
    
    // Format passenger name (lastname/firstname)
    $formattedName = strtoupper($lastName) . '/' . strtoupper($firstName);
    
    // Format flight number (remove spaces)
    $formattedFlight = str_replace(' ', '', $flight);
    
    // Create the IATA data string according to BCBP standard
    $iataData = [
        'M1', // Format identifier
        $formattedName,
        'E', // Electronic ticket indicator
        'ABC123', // PNR code
        strtoupper($from) . strtoupper($to), // Route
        $formattedFlight,
        $julianDate, // Julian date
        $classCode,
        strtoupper($seat), // Seat number
        '001A', // Check-in sequence
        '0001', // Passenger status
        '0' // Version number
    ];
    
    return implode('', $iataData);
}

// Class code mapping
$classCodes = [
    'Y' => 'Economy',
    'W' => 'Premium Economy',
    'J' => 'Business',
    'F' => 'First'
];

// Generate IATA data
$iataData = formatBoardingPassData(
    $data['firstName'],
    $data['lastName'],
    $data['flight'],
    $data['from'],
    $data['to'],
    $flightDate,
    $data['seat'],
    $data['class']
);

// Get class name from code
$className = $classCodes[$data['class']] ?? 'Economy';

// Prepare display data
$displayData = [
    'name' => strtoupper($data['firstName'] . ' ' . $data['lastName']),
    'flight' => strtoupper($data['flight']),
    'from' => strtoupper($data['from']),
    'to' => strtoupper($data['to']),
    'date' => strtoupper($flightDate->format('d M Y')),
    'time' => $data['time'],
    'seat' => strtoupper($data['seat']),
    'class' => strtoupper($className . ' (' . $data['class'] . ')')
];

// Store document in database
try {
    $pdo = getDB();
    $stmt = $pdo->prepare("
        INSERT INTO documents (type, data, iata_data, display_data) 
        VALUES (?, ?, ?, ?)
    ");
    
    $stmt->execute([
        'boardingPass',
        json_encode($data),
        $iataData,
        json_encode($displayData)
    ]);
    
    $documentId = $pdo->lastInsertId();
    
    // Return success response
    sendResponse([
        'success' => true,
        'documentId' => $documentId,
        'document' => [
            'type' => 'boardingPass',
            'data' => $data,
            'iataData' => $iataData,
            'displayData' => $displayData
        ]
    ]);
    
} catch (PDOException $e) {
    sendError('Database error: ' . $e->getMessage(), 500);
}
?>