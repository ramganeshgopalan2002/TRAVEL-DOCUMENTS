<?php
require_once 'config.php';

// Get the requested URL
$url = isset($_GET['url']) ? $_GET['url'] : '';
$url = rtrim($url, '/');
$urlParts = explode('/', $url);

// Route the request
$endpoint = $urlParts[0] ?? '';

switch ($_SERVER['REQUEST_METHOD']) {
    case 'GET':
        switch ($endpoint) {
            case 'documents':
                require 'documents.php';
                break;
            case 'health-check':
                require 'health-check.php';
                break;
            case 'qr-code':
                require 'qr-code.php';
                break;
            case 'barcode':
                require 'barcode.php';
                break;
            default:
                sendError('Endpoint not found', 404);
        }
        break;
        
    case 'POST':
        switch ($endpoint) {
            case 'generate':
                $documentType = $urlParts[1] ?? '';
                switch ($documentType) {
                    case 'boarding-pass':
                        require 'boarding-pass.php';
                        break;
                    case 'e-ticket':
                        require 'e-ticket.php';
                        break;
                    case 'baggage-tag':
                        require 'baggage-tag.php';
                        break;
                    default:
                        sendError('Document type not specified', 400);
                }
                break;
            case 'documents':
                $documentId = $urlParts[1] ?? '';
                if ($documentId) {
                    require 'documents.php';
                } else {
                    sendError('Document ID not specified', 400);
                }
                break;
            default:
                sendError('Endpoint not found', 404);
        }
        break;
        
    case 'DELETE':
        if ($endpoint === 'documents') {
            $documentId = $urlParts[1] ?? '';
            if ($documentId) {
                require 'documents.php';
            } else {
                sendError('Document ID not specified', 400);
            }
        } else {
            sendError('Endpoint not found', 404);
        }
        break;
        
    default:
        sendError('Method not allowed', 405);
}
?>