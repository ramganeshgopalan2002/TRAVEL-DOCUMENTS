// Generate barcode for IATA boarding pass - CORRECTED VERSION
const iataBarcodeSvg = document.getElementById('iataBarcode');
// Clear existing content but keep the SVG element structure
iataBarcodeSvg.innerHTML = '';

// Use setTimeout to ensure DOM is ready
setTimeout(() => {
    try {
        JsBarcode("#iataBarcode", bcbpData, {
            format: "CODE128",
            width: 2,
            height: 50,
            displayValue: false,
            background: "#ffffff",
            lineColor: "#000000"
        });
    } catch (error) {
        console.error('Barcode generation error:', error);
        // Fallback: Show error message
        iataBarcodeSvg.innerHTML = '<text x="50%" y="50%" text-anchor="middle" fill="red">Barcode Error</text>';
    }
}, 100);