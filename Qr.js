// Generate QR code for boarding pass - CORRECTED VERSION
const iataQrCode = document.getElementById('iataQrCode');
iataQrCode.innerHTML = ''; // Clear existing content

// Create a canvas element for the QR code
const qrCanvas = document.createElement('canvas');
iataQrCode.appendChild(qrCanvas);

// Generate QR code using the correct method
QRCode.toCanvas(qrCanvas, qrData, {
    width: 100,
    margin: 1,
    color: {
        dark: '#000000',
        light: '#ffffff'
    }
}, function(error) {
    if (error) {
        console.error('QR Code generation error:', error);
        // Fallback: Show error message
        iataQrCode.innerHTML = '<p style="color:red; font-size:10px;">QR Code Error</p>';
    }
});