<?php
require_once 'config.php';

// Only handle POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    sendError('Method not allowed', 405);
}

$data = getJsonInput();

// Validate required fields
$requiredFields = ['ticketNumber', 'firstName', 'lastName', 'flight', 'from', 'to', 'date', 'time'];
foreach ($requiredFields as $field) {
    if (!isset($data[$field]) || empty($data[$field])) {
        sendError("Missing required field: $field");
    }
}

// Validate ticket number
if (strlen($data['ticketNumber']) < 13) {
    sendError('Ticket number must be at least 13 digits');
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

// Generate e-ticket data
function formatETicketData($ticketNumber, $firstName, $lastName, $flight, $from, $to, $date) {
    // Format the date in YYMMDD format
    $dateStr = $date->format('ymd');
    
    // Format flight number (remove spaces)
    $formattedFlight = str_replace(' ', '', $flight);
    
    // Create e-ticket data
    $eTicketData = [
        $ticketNumber,
        strtoupper($firstName . ' ' . $lastName),
        $formattedFlight,
        strtoupper($from) . strtoupper($to),
        $dateStr
    ];
    
    return implode('|', $eTicketData);
}

// Airline code mapping
$airlineCodes = [
    'UA' => 'UNITED AIRLINES',
    'AA' => 'AMERICAN AIRLINES',
    'DL' => 'DELTA AIR LINES',
    'LH' => 'LUFTHANSA',
    'BA' => 'BRITISH AIRWAYS',
    'AF' => 'AIR FRANCE'
];

// Generate IATA data
$iataData = formatETicketData(
    $data['ticketNumber'],
    $data['firstName'],
    $data['lastName'],
    $data['flight'],
    $data['from'],
    $data['to'],
    $flightDate
);

// Get airline code from flight number
$airlineCode = substr(strtoupper($data['flight']), 0, 2);
$airlineName = $airlineCodes[$airlineCode] ?? $airlineCode;

// Format ticket number with space
$formattedTicketNumber = substr($data['ticketNumber'], 0, 3) . ' ' . substr($data['ticketNumber'], 3);

// Prepare display data
$displayData = [
    'ticketNumber' => $formattedTicketNumber,
    'airline' => $airlineName,
    'name' => strtoupper($data['firstName'] . ' ' . $data['lastName']),
    'flight' => strtoupper($data['flight']),
    'date' => strtoupper($flightDate->format('d M Y')),
    'from' => strtoupper($data['from']),
    'to' => strtoupper($data['to']),
    'time' => $data['time'],
    'status' => 'CONFIRMED'
];

// Store document in database
try {
    $pdo = getDB();
    $stmt = $pdo->prepare("
        INSERT INTO documents (type, data, iata_data, display_data) 
        VALUES (?, ?, ?, ?)
    ");
    
    $stmt->execute([
        'eTicket',
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
            'type' => 'eTicket',
            'data' => $data,
            'iataData' => $iataData,
            'displayData' => $displayData
        ]
    ]);
    
} catch (PDOException $e) {
    sendError('Database error: ' . $e->getMessage(), 500);
}
?>