<?php
require_once 'config.php';

try {
    $pdo = getDB();
    
    // Handle GET request (get all documents or specific document)
    if ($_SERVER['REQUEST_METHOD'] === 'GET') {
        if (isset($_GET['id'])) {
            // Get specific document
            $stmt = $pdo->prepare("SELECT * FROM documents WHERE id = ?");
            $stmt->execute([$_GET['id']]);
            $document = $stmt->fetch(PDO::FETCH_ASSOC);
            
            if (!$document) {
                sendError('Document not found', 404);
            }
            
            // Decode JSON fields
            $document['data'] = json_decode($document['data'], true);
            $document['display_data'] = json_decode($document['display_data'], true);
            
            sendResponse([
                'success' => true,
                'document' => $document
            ]);
        } else {
            // Get all documents
            $stmt = $pdo->query("SELECT * FROM documents ORDER BY created_at DESC");
            $documents = $stmt->fetchAll(PDO::FETCH_ASSOC);
            
            // Decode JSON fields for each document
            foreach ($documents as &$document) {
                $document['data'] = json_decode($document['data'], true);
                $document['display_data'] = json_decode($document['display_data'], true);
            }
            
            sendResponse([
                'success' => true,
                'documents' => $documents
            ]);
        }
    }
    // Handle DELETE request
    elseif ($_SERVER['REQUEST_METHOD'] === 'DELETE') {
        $urlParts = explode('/', $_GET['url']);
        $documentId = $urlParts[1] ?? null;
        
        if (!$documentId) {
            sendError('Document ID not specified', 400);
        }
        
        $stmt = $pdo->prepare("DELETE FROM documents WHERE id = ?");
        $stmt->execute([$documentId]);
        
        if ($stmt->rowCount() > 0) {
            sendResponse(['success' => true]);
        } else {
            sendError('Document not found', 404);
        }
    }
    // Handle unsupported methods
    else {
        sendError('Method not allowed', 405);
    }
    
} catch (PDOException $e) {
    sendError('Database error: ' . $e->getMessage(), 500);
}
?>