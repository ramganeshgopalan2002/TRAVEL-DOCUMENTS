<?php
// api.php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
    exit(0);
}

require_once 'vendor/autoload.php';

use Endroid\QrCode\QrCode;
use Endroid\QrCode\Writer\PngWriter;
use Picqer\Barcode\BarcodeGeneratorPNG;

// QR Code Generation Endpoint
if ($_POST['action'] == 'generate-qr-code') {
    try {
        $data = json_decode(file_get_contents('php://input'), true);
        
        // Create QR code data
        $qrData = "";
        if (isset($data['flight']) && isset($data['fromAirport'])) {
            $qrData = "FLIGHT:{$data['flight']}|FROM:{$data['fromAirport']}|TO:{$data['toAirport']}|DATE:{$data['date']}|TIME:{$data['time']}|PASSENGER:{$data['passengerName']}|SEAT:{$data['seat']}|PNR:{$data['pnr']}";
        } elseif (isset($data['ticketNumber'])) {
            $qrData = "TICKET:{$data['ticketNumber']}|FLIGHT:{$data['etFlight']}|FROM:{$data['etFrom']}|TO:{$data['etTo']}|DATE:{$data['etDate']}|TIME:{$data['etTime']}|PASSENGER:{$data['etFirstName']} {$data['etLastName']}|PNR:{$data['pnrEt']}";
        } else {
            $qrData = json_encode($data);
        }

        // Generate QR code
        $qrCode = QrCode::create($qrData)
            ->setSize(200)
            ->setMargin(10);

        $writer = new PngWriter();
        $result = $writer->write($qrCode);
        
        $qrCodeData = base64_encode($result->getString());
        
        echo json_encode([
            'success' => true,
            'data' => [
                'qrImageUrl' => 'data:image/png;base64,' . $qrCodeData,
                'qrData' => $qrData
            ]
        ]);
        
    } catch (Exception $e) {
        http_response_code(500);
        echo json_encode([
            'success' => false,
            'error' => $e->getMessage()
        ]);
    }
}

// Barcode Generation Endpoint
elseif ($_POST['action'] == 'generate-barcode') {
    try {
        $data = json_decode(file_get_contents('php://input'), true);
        
        // Determine barcode data
        $barcodeData = "";
        if (isset($data['pnr'])) {
            $barcodeData = $data['pnr'];
        } elseif (isset($data['bagNumber'])) {
            $barcodeData = $data['bagNumber'];
        } elseif (isset($data['ticketNumber'])) {
            $barcodeData = $data['ticketNumber'];
        } else {
            $barcodeData = "1234567890";
        }

        // Generate barcode
        $generator = new BarcodeGeneratorPNG();
        $barcodeImage = $generator->getBarcode($barcodeData, $generator::TYPE_CODE_128);
        
        $barcodeData = base64_encode($barcodeImage);
        
        echo json_encode([
            'success' => true,
            'data' => [
                'barcodeImageUrl' => 'data:image/png;base64,' . $barcodeData,
                'barcodeData' => $barcodeData
            ]
        ]);
        
    } catch (Exception $e) {
        http_response_code(500);
        echo json_encode([
            'success' => false,
            'error' => $e->getMessage()
        ]);
    }
}

// Health check
elseif ($_GET['action'] == 'health') {
    echo json_encode([
        'status' => 'OK',
        'message' => 'Travel Document API is running'
    ]);
}

else {
    http_response_code(404);
    echo json_encode([
        'success' => false,
        'error' => 'Endpoint not found'
    ]);
}
?>