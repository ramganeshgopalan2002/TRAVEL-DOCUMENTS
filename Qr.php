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

// Include QR code library
require_once 'phpqrcode/qrlib.php';

// Generate QR code and output directly as PNG
QRcode::png($data, false, QR_ECLEVEL_L, 10, 1);
exit();
?>