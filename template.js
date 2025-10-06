// Replace the existing generateDocument function with this updated version
async function generateDocument() {
    const generateBtn = document.getElementById('generateBtn');
    const statusMessage = document.getElementById('statusMessage');

    generateBtn.disabled = true;
    generateBtn.textContent = 'Generating...';
    statusMessage.classList.remove('show', 'success', 'error', 'warning');

    const data = {};
    if (currentMode === 'eTicket') {
        data.ticketNumber = formElements.ticketNumber.value || '0161234567890';
        data.pnrEt = formElements.pnrEt.value || 'ABC123';
        data.etFirstName = formElements.etFirstName.value || 'John';
        data.etLastName = formElements.etLastName.value || 'Doe';
        data.etFlight = formElements.etFlight.value || 'PR 2727';
        data.etFrom = formElements.etFrom.value || 'PHIL';
        data.etTo = formElements.etTo.value || 'CEB';
        data.etDate = formElements.etDate.value || '2025-09-10';
        data.etTime = formElements.etTime.value || '13:15';
        data.etArrivalDate = formElements.etArrivalDate.value || '2025-09-10';
        data.etArrivalTime = formElements.etArrivalTime.value || '15:35';
    } else if (currentMode === 'baggageTag') {
        data.bagFirstName = formElements.bagFirstName.value || 'John';
        data.bagLastName = formElements.bagLastName.value || 'Doe';
        data.bagPnr = formElements.bagPnr.value || 'ABC123';
        data.bagFlight = formElements.bagFlight.value || 'PR 2727';
        data.bagFrom = formElements.bagFrom.value || 'PHIL';
        data.bagTo = formElements.bagTo.value || 'CEB';
        data.bagWeight = formElements.bagWeight.value || '23';
        data.bagNumber = formElements.bagNumber.value || '1234567890';
    } else {
        // Boarding pass and mobile pass
        data.firstName = formElements.firstName.value || 'John';
        data.lastName = formElements.lastName.value || 'Doe';
        data.pnr = formElements.pnr.value || 'ABC123';
        data.flight = formElements.flight.value || 'PR 2727';
        data.from = formElements.from.value || 'PHIL';
        data.to = formElements.to.value || 'CEB';
        data.fromTerminal = formElements.fromTerminal.value || 'T1';
        data.toTerminal = formElements.toTerminal.value || 'T1';
        data.date = formElements.date.value || '2025-09-10';
        data.time = formElements.time.value || '13:15';
        data.arrivalDate = formElements.arrivalDate.value || '2025-09-10';
        data.arrivalTime = formElements.arrivalTime.value || '15:35';
        data.boardingTime = formElements.boardingTime.value || '12:45';
        data.seat = formElements.seat.value || '17A';
        data.gate = formElements.gate.value || '07';
        data.class = formElements.class.value || 'Y';
        data.sequence = formElements.sequence.value || '001A';
    }

    try {
        // Send data to backend for QR code generation
        const qrResponse = await fetch('/api/generate/qr-code', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const qrResult = await qrResponse.json();

        // Send data to backend for barcode generation
        const barcodeResponse = await fetch('/api/generate/barcode', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const barcodeResult = await barcodeResponse.json();

        if (qrResult.success && barcodeResult.success) {
            const combinedData = {
                ...data,
                qrImageUrl: qrResult.data.qrImageUrl,
                barcodeImageUrl: barcodeResult.data.barcodeImageUrl,
                barcodeData: barcodeResult.data.barcodeData
            };
            
            // Add passenger name for all modes
            if (currentMode === 'eTicket') {
                combinedData.passengerName = `${data.etFirstName} ${data.etLastName}`.toUpperCase();
                combinedData.firstName = data.etFirstName;
                combinedData.lastName = data.etLastName;
            } else if (currentMode === 'baggageTag') {
                combinedData.passengerName = `${data.bagFirstName} ${data.bagLastName}`.toUpperCase();
                combinedData.firstName = data.bagFirstName;
                combinedData.lastName = data.bagLastName;
            } else {
                combinedData.passengerName = `${data.firstName} ${data.lastName}`.toUpperCase();
            }
            
            formatAndDisplay(combinedData);
            showMessage('Document generated successfully!', 'success');
        } else {
            throw new Error('Failed to generate one or more codes.');
        }
    } catch (error) {
        console.error('Error:', error);
        showMessage('Error generating document. Please try again.', 'error');
    } finally {
        generateBtn.disabled = false;
        generateBtn.textContent = 'Generate Document';
    }
}

// Update the formatAndDisplay function to handle barcode numbers
function formatAndDisplay(data) {
    previewInstruction.classList.add('hidden');
    
    // Set barcode number for all modes
    if (currentMode === 'boardingPass' || currentMode === 'mobilePass') {
        // ... existing code ...
        
        if (currentMode === 'boardingPass') {
            // ... existing code ...
            document.getElementById('iataBarcodeNumber').textContent = data.barcodeData || data.pnr;
        } else if (currentMode === 'mobilePass') {
            // ... existing code ...
            document.getElementById('mobileBarcodeNumber').textContent = data.barcodeData || data.pnr;
        }
    } else if (currentMode === 'eTicket') {
        // ... existing code ...
    } else if (currentMode === 'baggageTag') {
        // ... existing code ...
        document.getElementById('bagTagBarcodeNumber').textContent = data.barcodeData || data.bagNumber;
    }
}