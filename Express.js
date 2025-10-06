// server.js
const express = require('express');
const QRCode = require('qrcode');
const JsBarcode = require('jsbarcode');
const { createCanvas } = require('canvas');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// QR Code Generation Endpoint
app.post('/api/generate/qr-code', async (req, res) => {
    try {
        const data = req.body;
        
        // Create QR code data string based on document type
        let qrData = '';
        
        if (data.flight && data.fromAirport) {
            // Boarding Pass/Mobile Pass
            qrData = `FLIGHT:${data.flight}|FROM:${data.fromAirport}|TO:${data.toAirport}|DATE:${data.date}|TIME:${data.time}|PASSENGER:${data.passengerName || `${data.firstName} ${data.lastName}`}|SEAT:${data.seat}|PNR:${data.pnr}`;
        } else if (data.ticketNumber) {
            // E-Ticket
            qrData = `TICKET:${data.ticketNumber}|FLIGHT:${data.etFlight}|FROM:${data.etFrom}|TO:${data.etTo}|DATE:${data.etDate}|TIME:${data.etTime}|PASSENGER:${data.etFirstName} ${data.etLastName}|PNR:${data.pnrEt}`;
        } else {
            qrData = JSON.stringify(data);
        }

        // Generate QR code as data URL
        const qrCodeDataURL = await QRCode.toDataURL(qrData, {
            width: 200,
            margin: 2,
            color: {
                dark: '#183D5E',
                light: '#FFFFFF'
            }
        });

        res.json({
            success: true,
            data: {
                qrImageUrl: qrCodeDataURL,
                qrData: qrData
            }
        });
    } catch (error) {
        console.error('QR Code generation error:', error);
        res.status(500).json({
            success: false,
            error: 'Failed to generate QR code'
        });
    }
});

// Barcode Generation Endpoint
app.post('/api/generate/barcode', async (req, res) => {
    try {
        const data = req.body;
        
        // Determine what to encode in barcode
        let barcodeData = '';
        
        if (data.pnr) {
            barcodeData = data.pnr;
        } else if (data.bagNumber) {
            barcodeData = data.bagNumber;
        } else if (data.ticketNumber) {
            barcodeData = data.ticketNumber;
        } else {
            barcodeData = '1234567890'; // Default fallback
        }

        // Create canvas for barcode
        const canvas = createCanvas(300, 100);
        
        // Generate barcode
        JsBarcode(canvas, barcodeData, {
            format: "CODE128",
            width: 2,
            height: 50,
            displayValue: false,
            margin: 10
        });

        // Convert to data URL
        const barcodeDataURL = canvas.toDataURL();

        res.json({
            success: true,
            data: {
                barcodeImageUrl: barcodeDataURL,
                barcodeData: barcodeData
            }
        });
    } catch (error) {
        console.error('Barcode generation error:', error);
        res.status(500).json({
            success: false,
            error: 'Failed to generate barcode'
        });
    }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
    res.json({ status: 'OK', message: 'Travel Document API is running' });
});

// Serve frontend
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
    console.log(`API endpoints available at http://localhost:${PORT}/api/`);
});