// Initialize jsPDF
window.jsPDF = window.jspdf.jsPDF;

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const elements = {
        serverStatus: document.getElementById('serverStatus'),
        boardingPassBtn: document.getElementById('boardingPassBtn'),
        eTicketBtn: document.getElementById('eTicketBtn'),
        baggageTagBtn: document.getElementById('baggageTagBtn'),
        mobileToggleBtn: document.getElementById('mobileToggle'),
        boardingPassForm: document.getElementById('boardingPassForm'),
        eTicketForm: document.getElementById('eTicketForm'),
        baggageTagForm: document.getElementById('baggageTagForm'),
        iataBoardingPass: document.getElementById('iataBoardingPass'),
        eTicket: document.getElementById('eTicket'),
        baggageTag: document.getElementById('baggageTag'),
        formTitle: document.getElementById('formTitle'),
        previewTitle: document.getElementById('previewTitle'),
        previewInstruction: document.getElementById('previewInstruction'),
        downloadPdfBtn: document.getElementById('downloadPdf'),
        generateBtn: document.getElementById('generateBtn'),
        statusMessage: document.getElementById('statusMessage'),
        container: document.querySelector('.container')
    };

    // Configuration
    const config = {
        currentMode: 'boardingPass',
        airportCities: {
            'DEL': 'DELHI', 'BOM': 'MUMBAI', 'BLR': 'BANGALORE',
            'MAA': 'CHENNAI', 'HYD': 'HYDERABAD', 'CCU': 'KOLKATA',
            'AMD': 'AHMEDABAD', 'GOI': 'GOA', 'PNQ': 'PUNE', 'COK': 'KOCHI'
        }
    };

    // Initialize application
    init();

    function init() {
        setupEventListeners();
        setDefaultDates();
        checkServerHealth();
        generateDocument();
        elements.previewInstruction.style.display = 'none';
    }

    function setupEventListeners() {
        // Mode selection
        elements.boardingPassBtn.addEventListener('click', () => setMode('boardingPass'));
        elements.eTicketBtn.addEventListener('click', () => setMode('eTicket'));
        elements.baggageTagBtn.addEventListener('click', () => setMode('baggageTag'));
        
        // Mobile view toggle
        elements.mobileToggleBtn.addEventListener('click', toggleMobileView);
        
        // Generate document
        elements.generateBtn.addEventListener('click', handleGenerateDocument);
        
        // PDF download
        elements.downloadPdfBtn.addEventListener('click', handlePdfDownload);
        
        // Weather update on destination change
        document.getElementById('to').addEventListener('change', function() {
            updateWeather(this.value);
        });
    }

    // Server Functions
    async function checkServerHealth() {
        try {
            const response = await fetch('/api/health');
            if (response.ok) {
                setServerStatus('Server Connected', 'connected');
            } else {
                throw new Error('Server not responding properly');
            }
        } catch (error) {
            setServerStatus('Server Disconnected', 'disconnected');
            console.error('Server health check failed:', error);
        }
    }

    function setServerStatus(message, status) {
        elements.serverStatus.textContent = message;
        elements.serverStatus.className = `server-status ${status}`;
    }

    // Mode Management
    function setMode(mode) {
        config.currentMode = mode;
        
        // Update active button
        document.querySelectorAll('.mode-btn').forEach(btn => btn.classList.remove('active'));
        elements[`${mode}Btn`].classList.add('active');
        
        // Hide all forms and previews
        hideAllElements([elements.boardingPassForm, elements.eTicketForm, elements.baggageTagForm,
                        elements.iataBoardingPass, elements.eTicket, elements.baggageTag]);
        
        // Show selected mode
        showSelectedMode(mode);
        
        // Generate document for current mode
        generateDocument();
    }

    function hideAllElements(elementsArray) {
        elementsArray.forEach(element => element.classList.add('hidden'));
    }

    function showSelectedMode(mode) {
        const modeConfig = {
            boardingPass: {
                form: elements.boardingPassForm,
                preview: elements.iataBoardingPass,
                formTitle: 'Passenger & Flight Details',
                previewTitle: 'Your IATA Boarding Pass'
            },
            eTicket: {
                form: elements.eTicketForm,
                preview: elements.eTicket,
                formTitle: 'E-Ticket Details',
                previewTitle: 'Your E-Ticket'
            },
            baggageTag: {
                form: elements.baggageTagForm,
                preview: elements.baggageTag,
                formTitle: 'Baggage Details',
                previewTitle: 'Your Baggage Tag'
            }
        };

        const config = modeConfig[mode];
        config.form.classList.remove('hidden');
        config.preview.classList.remove('hidden');
        elements.formTitle.textContent = config.formTitle;
        elements.previewTitle.textContent = config.previewTitle;
    }

    // Mobile View
    function toggleMobileView() {
        elements.container.classList.toggle('mobile-view');
        elements.mobileToggleBtn.textContent = elements.container.classList.contains('mobile-view') 
            ? 'Desktop View' 
            : 'Mobile View';
    }

    // Document Generation
    async function handleGenerateDocument() {
        try {
            setButtonState(true, 'Generating...');
            await generateDocument();
            showStatus('Document generated successfully!', 'success');
            elements.previewInstruction.style.display = 'none';
        } catch (error) {
            showStatus('Error generating document: ' + error.message, 'error');
        } finally {
            setButtonState(false, 'Generate Document');
        }
    }

    function setButtonState(disabled, text) {
        elements.generateBtn.disabled = disabled;
        elements.generateBtn.textContent = text;
    }

    async function generateDocument() {
        const generators = {
            boardingPass: generateBoardingPass,
            eTicket: generateETicket,
            baggageTag: generateBaggageTag
        };
        
        await generators[config.currentMode]();
    }

    // Boarding Pass Generator
    async function generateBoardingPass() {
        const formData = getFormData('boardingPass');
        const { firstName, lastName, pnr, flight, from, fromTerminal, to, toTerminal, 
                date, time, arrivalDate, arrivalTime, boardingTime, seat, class: flightClass, 
                sequence, gate } = formData;

        const passengerName = formatPassengerName(firstName, lastName);
        const formattedDate = formatDateShort(date);
        const formattedArrivalDate = formatDateShort(arrivalDate);

        updateBoardingPassPreview({
            from, to, fromTerminal, toTerminal, formattedDate, formattedArrivalDate,
            time, arrivalTime, passengerName, flight, pnr, gate, seat, sequence, flightClass, boardingTime
        });

        await updateWeather(to);
        
        const qrData = generateBoardingPassQRData(formData, passengerName);
        await generateQRCode('iataQrCode', qrData, 100);
    }

    function getFormData(mode) {
        const fieldMappings = {
            boardingPass: [
                'firstName', 'lastName', 'pnr', 'flight', 'from', 'fromTerminal', 
                'to', 'toTerminal', 'date', 'time', 'arrivalDate', 'arrivalTime', 
                'boardingTime', 'seat', 'class', 'sequence', 'gate'
            ],
            eTicket: [
                'eticketNumber', 'eticketFirstName', 'eticketLastName', 'eticketFlight',
                'eticketFrom', 'eticketTo', 'eticketDate', 'eticketTime', 'eticketArrivalDate',
                'eticketArrivalTime', 'eticketClass', 'eticketFareBasis', 'eticketStatus'
            ],
            baggageTag: [
                'baggageFirstName', 'baggageLastName', 'baggageFlight', 'baggageFrom',
                'baggageTo', 'baggageDate', 'baggageTagNumber', 'baggageWeight', 'baggagePieces'
            ]
        };

        const data = {};
        fieldMappings[mode].forEach(field => {
            const element = document.getElementById(field);
            data[field.replace('eticket', '').replace('baggage', '')] = element ? element.value : '';
        });

        return data;
    }

    function updateBoardingPassPreview(data) {
        const {
            from, to, fromTerminal, toTerminal, formattedDate, formattedArrivalDate,
            time, arrivalTime, passengerName, flight, pnr, gate, seat, sequence, flightClass, boardingTime
        } = data;

        // Update route section
        document.getElementById('iataFrom').textContent = from;
        document.getElementById('iataFromCity').textContent = config.airportCities[from] || from;
        document.getElementById('iataFromTerminal').textContent = `Terminal ${fromTerminal}`;
        document.getElementById('iataFromTime').textContent = `${formattedDate} ${formatTime(time)}`;

        document.getElementById('iataTo').textContent = to;
        document.getElementById('iataToCity').textContent = config.airportCities[to] || to;
        document.getElementById('iataToTerminal').textContent = `Terminal ${toTerminal}`;
        document.getElementById('iataToTime').textContent = `${formattedArrivalDate} ${formatTime(arrivalTime)}`;

        // Update passenger and flight details
        document.getElementById('iataPassenger').textContent = passengerName;
        document.getElementById('iataFlight').textContent = flight;
        document.getElementById('iataPnr').textContent = pnr;
        document.getElementById('iataGate').textContent = gate;
        document.getElementById('iataSeat').textContent = seat;
        document.getElementById('iataSequence').textContent = sequence;
        document.getElementById('iataClass').textContent = getClassText(flightClass).toUpperCase();
        document.getElementById('iataBoarding').textContent = formatTime(boardingTime);
    }

    // E-Ticket Generator
    async function generateETicket() {
        const formData = getFormData('eTicket');
        const { Number: eticketNumber, FirstName: firstName, LastName: lastName, 
                Flight: flight, From: from, To: to, Date: date, Time: time, 
                ArrivalDate: arrivalDate, ArrivalTime: arrivalTime, Class: flightClass, 
                FareBasis: fareBasis, Status: status } = formData;

        const passengerName = formatPassengerName(firstName, lastName);
        const formattedDate = formatDateShort(date);
        const formattedArrivalDate = formatDateShort(arrivalDate);

        updateETicketPreview({
            passengerName, eticketNumber, status, flight, flightClass,
            from, to, formattedDate, formattedArrivalDate, time, arrivalTime, fareBasis
        });

        const qrData = generateETicketQRData(formData, passengerName);
        await generateQRCode('eticketQrCode', qrData, 120);
    }

    function updateETicketPreview(data) {
        const {
            passengerName, eticketNumber, status, flight, flightClass,
            from, to, formattedDate, formattedArrivalDate, time, arrivalTime, fareBasis
        } = data;

        document.getElementById('eticketPassenger').textContent = passengerName;
        document.getElementById('eticketNumberDisplay').textContent = eticketNumber;
        document.getElementById('eticketStatusDisplay').textContent = status.toUpperCase();
        document.getElementById('eticketFlightDisplay').textContent = flight;
        document.getElementById('eticketClassDisplay').textContent = getClassText(flightClass).toUpperCase();
        document.getElementById('eticketFromDisplay').textContent = `${from} - ${config.airportCities[from] || from}`;
        document.getElementById('eticketToDisplay').textContent = `${to} - ${config.airportCities[to] || to}`;
        document.getElementById('eticketDepartDisplay').textContent = `${formattedDate} ${formatTime(time)}`;
        document.getElementById('eticketArriveDisplay').textContent = `${formattedArrivalDate} ${formatTime(arrivalTime)}`;
        document.getElementById('eticketFareBasisDisplay').textContent = fareBasis;
    }

    // Baggage Tag Generator
    async function generateBaggageTag() {
        const formData = getFormData('baggageTag');
        const { FirstName: firstName, LastName: lastName, Flight: flight, 
                From: from, To: to, Date: date, TagNumber: tagNumber, 
                Weight: weight, Pieces: pieces } = formData;

        const passengerName = formatPassengerName(firstName, lastName);
        const formattedDate = formatDateShort(date);

        updateBaggageTagPreview({
            passengerName, flight, from, to, formattedDate, tagNumber, weight, pieces
        });

        generateBarcode('baggageBarcode', tagNumber);
    }

    function updateBaggageTagPreview(data) {
        const { passengerName, flight, from, to, formattedDate, tagNumber, weight, pieces } = data;

        document.getElementById('baggagePassenger').textContent = passengerName;
        document.getElementById('baggageFlightDisplay').textContent = flight;
        document.getElementById('baggageFromDisplay').textContent = from;
        document.getElementById('baggageToDisplay').textContent = to;
        document.getElementById('baggageDateDisplay').textContent = formattedDate;
        document.getElementById('baggageTagNumberDisplay').textContent = tagNumber;
        document.getElementById('baggageWeightDisplay').textContent = `${weight} KG`;
        document.getElementById('baggagePiecesDisplay').textContent = pieces;
        document.getElementById('baggageFinalDestination').textContent = `${to} - ${config.airportCities[to] || to}`;
    }

    // Weather Functions
    async function updateWeather(destinationCode) {
        try {
            const weather = await fetchWeatherData(destinationCode);
            const updatedTime = new Date(weather.timestamp).toLocaleTimeString();
            
            document.getElementById('weatherIcon').textContent = weather.emoji;
            document.getElementById('weatherTemp').textContent = `${weather.temperature}°C`;
            document.getElementById('weatherDesc').textContent = weather.description;
            document.getElementById('weatherLocation').textContent = weather.city;
            document.getElementById('weatherUpdated').textContent = `Updated: ${updatedTime}`;
        } catch (error) {
            console.error('Weather update error:', error);
            setDefaultWeather(destinationCode);
        }
    }

    async function fetchWeatherData(cityCode) {
        try {
            const response = await fetch(`/api/weather/${cityCode}`);
            if (!response.ok) throw new Error('Weather API not responding');
            
            const data = await response.json();
            if (data.success) {
                return {
                    temperature: data.temperature,
                    description: data.description,
                    emoji: data.emoji,
                    city: data.city,
                    timestamp: data.timestamp
                };
            } else {
                throw new Error(data.error || 'Weather data unavailable');
            }
        } catch (error) {
            console.error('Weather API Error:', error);
            return getFallbackWeatherData(cityCode);
        }
    }

    function getFallbackWeatherData(cityCode) {
        return {
            temperature: 25,
            description: 'Weather unavailable',
            emoji: '🌤️',
            city: config.airportCities[cityCode] || cityCode,
            timestamp: new Date().toISOString()
        };
    }

    function setDefaultWeather(destinationCode) {
        document.getElementById('weatherIcon').textContent = '🌤️';
        document.getElementById('weatherTemp').textContent = '25°C';
        document.getElementById('weatherDesc').textContent = 'Weather unavailable';
        document.getElementById('weatherLocation').textContent = config.airportCities[destinationCode] || destinationCode;
        document.getElementById('weatherUpdated').textContent = 'Updated: Failed';
    }

    // QR Code Generation
    function generateBoardingPassQRData(formData, passengerName) {
        const { pnr, flight, from, to, date, time, seat, class: flightClass, sequence, gate } = formData;
        
        return `BOARDING PASS:
Passenger: ${passengerName}
Flight: ${flight}
From: ${from} To: ${to}
Date: ${date} Time: ${time}
Seat: ${seat} Class: ${getClassText(flightClass)}
PNR: ${pnr} Sequence: ${sequence}
Gate: ${gate}`;
    }

    function generateETicketQRData(formData, passengerName) {
        const { Number: eticketNumber, Flight: flight, From: from, To: to, 
                Date: date, Time: time, Class: flightClass, Status: status } = formData;
        
        return `E-TICKET:
Ticket: ${eticketNumber}
Passenger: ${passengerName}
Flight: ${flight}
Route: ${from} to ${to}
Date: ${date} Time: ${time}
Class: ${getClassText(flightClass)}
Status: ${status}`;
    }

    function generateQRCode(canvasId, data, size) {
        return new Promise((resolve, reject) => {
            const canvas = document.getElementById(canvasId);
            if (!canvas) {
                reject(new Error('Canvas element not found: ' + canvasId));
                return;
            }
            
            // Clear canvas
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Set dimensions
            canvas.width = size;
            canvas.height = size;
            
            QRCode.toCanvas(canvas, data, {
                width: size,
                margin: 1,
                color: { dark: '#000000', light: '#ffffff' }
            }, function(error) {
                if (error) {
                    console.error('QR Code generation error:', error);
                    reject(error);
                } else {
                    resolve();
                }
            });
        });
    }

    // Barcode Generation
    function generateBarcode(svgId, data) {
        try {
            JsBarcode(`#${svgId}`, data, {
                format: "CODE128",
                width: 2,
                height: 50,
                displayValue: false,
                background: "transparent",
                lineColor: "#000000"
            });
        } catch (error) {
            console.error('Barcode generation error:', error);
            const svg = document.getElementById(svgId);
            svg.innerHTML = `<text x="50%" y="50%" text-anchor="middle" alignment-baseline="middle" 
                                font-family="monospace" font-size="10">${data}</text>`;
        }
    }

    // PDF Generation
    async function handlePdfDownload() {
        try {
            const { element, filename } = getDownloadConfig();
            await generatePDF(element, filename);
            showStatus('PDF download started!', 'success');
        } catch (error) {
            showStatus('Error generating PDF: ' + error.message, 'error');
        }
    }

    function getDownloadConfig() {
        const modes = {
            boardingPass: {
                element: elements.iataBoardingPass,
                firstName: document.getElementById('firstName').value || 'Rahul',
                lastName: document.getElementById('lastName').value || 'Sharma',
                prefix: 'boardingPass'
            },
            eTicket: {
                element: elements.eTicket,
                firstName: document.getElementById('eticketFirstName').value || 'Rahul',
                lastName: document.getElementById('eticketLastName').value || 'Sharma',
                prefix: 'eTicket'
            },
            baggageTag: {
                element: elements.baggageTag,
                firstName: document.getElementById('baggageFirstName').value || 'Rahul',
                lastName: document.getElementById('baggageLastName').value || 'Sharma',
                prefix: 'baggageTag'
            }
        };

        const mode = modes[config.currentMode];
        const filename = `${mode.prefix}_${mode.firstName}_${mode.lastName}.pdf`;
        
        return { element: mode.element, filename };
    }

    async function generatePDF(element, filename) {
        try {
            const elementClone = element.cloneNode(true);
            elementClone.style.cssText = 'position:fixed; left:0; top:0; z-index:9999; transform:scale(1);';
            document.body.appendChild(elementClone);
            
            await waitForImages(elementClone);
            
            const canvas = await html2canvas(elementClone, {
                scale: 3,
                useCORS: true,
                allowTaint: false,
                backgroundColor: '#ffffff',
                logging: false
            });
            
            const imgData = canvas.toDataURL('image/png', 1.0);
            const pdf = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a6' });
            
            const imgWidth = 100;
            const imgHeight = canvas.height * imgWidth / canvas.width;
            const xPos = (105 - imgWidth) / 2;
            const yPos = 10;
            
            pdf.addImage(imgData, 'PNG', xPos, yPos, imgWidth, imgHeight);
            pdf.save(filename);
            
            document.body.removeChild(elementClone);
            
        } catch (error) {
            console.error('PDF generation error:', error);
            cleanupClones();
            throw new Error('PDF generation failed: ' + error.message);
        }
    }

    function waitForImages(element) {
        return new Promise((resolve) => {
            const images = element.querySelectorAll('img, canvas, svg');
            let loadedCount = 0;
            const totalImages = images.length;
            
            if (totalImages === 0) {
                resolve();
                return;
            }
            
            function checkAllLoaded() {
                loadedCount++;
                if (loadedCount === totalImages) resolve();
            }
            
            images.forEach(img => {
                if (img.complete && img.naturalHeight !== 0) {
                    checkAllLoaded();
                } else if (img.tagName === 'CANVAS' || img.tagName === 'SVG') {
                    checkAllLoaded();
                } else {
                    img.addEventListener('load', checkAllLoaded);
                    img.addEventListener('error', checkAllLoaded);
                }
            });
            
            setTimeout(resolve, 3000);
        });
    }

    function cleanupClones() {
        const clones = document.querySelectorAll('[style*="fixed"]');
        clones.forEach(clone => {
            if (clone !== elements.iataBoardingPass && clone !== elements.eTicket && clone !== elements.baggageTag) {
                document.body.removeChild(clone);
            }
        });
    }

    // Utility Functions
    function formatPassengerName(firstName, lastName) {
        return (firstName + ' ' + lastName).toUpperCase();
    }

    function formatDateShort(dateString) {
        const date = new Date(dateString);
        const options = { day: 'numeric', month: 'short' };
        return date.toLocaleDateString('en-US', options).toUpperCase();
    }

    function formatTime(timeString) {
        if (!timeString) return '';
        const [hours, minutes] = timeString.split(':');
        return `${hours}:${minutes}`;
    }

    function getClassText(classCode) {
        const classMap = {
            'Y': 'Economy',
            'W': 'Premium Economy',
            'J': 'Business',
            'F': 'First'
        };
        return classMap[classCode] || 'Economy';
    }

    function setDefaultDates() {
        const today = new Date();
        const tomorrow = new Date(today);
        tomorrow.setDate(tomorrow.getDate() + 1);
        
        const dateFields = ['date', 'arrivalDate', 'eticketDate', 'eticketArrivalDate', 'baggageDate'];
        dateFields.forEach((field, index) => {
            const element = document.getElementById(field);
            if (element) {
                element.value = index % 2 === 0 ? today.toISOString().split('T')[0] : tomorrow.toISOString().split('T')[0];
            }
        });
    }

    function showStatus(message, type) {
        elements.statusMessage.textContent = message;
        elements.statusMessage.className = `status-message show ${type}`;
        
        setTimeout(() => {
            elements.statusMessage.classList.remove('show');
        }, 3000);
    }
});