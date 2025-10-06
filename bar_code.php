<?php
require_once 'config.php';

// Only handle GET requests
if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    sendError('Method not allowed', 405);
}

// Get data from query parameter
if (!isset($_GET['data']) || empty($_GET['data'])) {
    sendError('Data parameter is required');
}

$data = $_GET['data'];

// Include barcode library
require_once 'vendor/autoload.php';

use Picqer\Barcode\BarcodeGeneratorPNG;

// Generate barcode
$generator = new BarcodeGeneratorPNG();
$barcode = $generator->getBarcode($data, $generator::TYPE_CODE_128);

// Output as PNG image
header('Content-Type: image/png');
echo $barcode;
exit();
?>