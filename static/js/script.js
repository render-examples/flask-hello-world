
const notesFreq = new Map([
    ['C4', 261.625],
    ['D4', 293.665],
    ['E4', 329.628],
    ['F4', 349.228],
    ['G4', 391.995],
    ['A4', 440],
    ['B4', 493.883],
    ['C5', 523.251],
    ['D5', 587.33],
    ['E5', 659.25],
    ['F5', 698.46],
    ['G5', 783.99],
    ['A5', 880.00],
    ['B5', 987.77],
    ['C6', 1046.50],
    ['D6', 1174.66],
    ['E6', 1318.51],
    ['F6', 1396.91],
    ['G6', 1567.98],
    ['A6', 1760.00],
    ['B6', 1975.53],
    ['C7', 2093.00]
]);



const container = document.querySelector('#container');

// Using forEach
notesFreq.forEach((value, key) => {
    const pianoKey = document.createElement('div');
    pianoKey.id = key;
    pianoKey.classList.add('piano-tile');
    pianoKey.innerText = key;
    container.appendChild(pianoKey);
});



const pianoTiles = document.querySelectorAll('.piano-tile');
// Function to start playing the note and change CSS

const activeOscillators = new Map();

function createOscillatorAndGainNode(pitch) {
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();

    // Define the harmonic content for the custom waveform
    const numberOfHarmonics = 4;
    const real = new Float32Array(numberOfHarmonics);
    const imag = new Float32Array(numberOfHarmonics);

    // DC offset and fundamental tone
    real[0] = 0; imag[0] = 0; // DC offset, not used for audio signal
    real[1] = 1; imag[1] = 0; // Fundamental tone

    // Harmonics
    real[2] = 0.8; imag[2] = 0; // First harmonic
    real[3] = 0.6; imag[3] = 0; // Second harmonic

    // Create the custom periodic waveform based on the defined harmonics
    const customWave = audioContext.createPeriodicWave(real, imag);
    oscillator.setPeriodicWave(customWave);

    oscillator.frequency.setValueAtTime(pitch, audioContext.currentTime);

    // ADSR Envelope
    gainNode.gain.setValueAtTime(0, audioContext.currentTime); // Start with no volume
    const attackTime = 0.02; // Attack
    gainNode.gain.linearRampToValueAtTime(1, audioContext.currentTime + attackTime); // Ramp to full volume

    const decayTime = 0.1; // Decay
    const sustainLevel = 0.65; // Sustain level
    gainNode.gain.linearRampToValueAtTime(sustainLevel, audioContext.currentTime + attackTime + decayTime); // Ramp to sustain level

    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);

    return { oscillator, gainNode };
}


function startNote() {
    const note = this.id;
    const pitch = notesFreq.get(note);
    this.classList.add('active');


    // Stop any existing note for this key
    if (activeOscillators.has(note)) {
        const existing = activeOscillators.get(note);
        existing.oscillator.stop();
        existing.oscillator.disconnect();
        existing.gainNode.disconnect();
    }

    const { oscillator, gainNode } = createOscillatorAndGainNode(pitch);
    oscillator.start();
    const noteEventId = Date.now();
    activeOscillators.set(note, { oscillator, gainNode, noteEventId });
}

function stopNote() {
    const note = this.id;
    this.classList.remove('active');
    const releaseTime = audioContext.currentTime;
    if (!activeOscillators.has(note)) {
        return;
    }
    if (activeOscillators.has(note)) {
        const { oscillator, gainNode, noteEventId } = activeOscillators.get(note);
        const decayDuration = 2;
        gainNode.gain.cancelScheduledValues(releaseTime);
        gainNode.gain.setValueAtTime(gainNode.gain.value, releaseTime); // New line to set current gain
        gainNode.gain.exponentialRampToValueAtTime(0.001, releaseTime + decayDuration);
        setTimeout(() => {
            // Check if the current note event is still the one that should be stopped
            if (activeOscillators.has(note) && activeOscillators.get(note).noteEventId === noteEventId) {
                oscillator.stop();
                oscillator.disconnect();
                gainNode.disconnect();
                activeOscillators.delete(note);
            }
        }, decayDuration * 1000);
    }
}


// PC touch event handler
let isMouseDown = false;

document.addEventListener('pointerdown', function (event) {
    if (event.buttons === 1) { // Check if left mouse button
        isMouseDown = true;
    }
}, false);
document.addEventListener('pointerup', function () {
    isMouseDown = false;
    // Optionally, stop the note here if you want notes to stop when the mouse is released
}, false);

for (const tile of pianoTiles) {
    tile.addEventListener('pointerdown', startNote);
    tile.addEventListener('pointerup', stopNote);
    tile.addEventListener('pointerover', function (event) {
        if (isMouseDown) {
            startNote.call(this, event); // Play note if mouse is down and pointer moves over a tile
        }
    });
    tile.addEventListener('pointerleave', stopNote);
}


// Create a new audio context
const audioContext = new (window.AudioContext || window.webkitAudioContext)();

// Variable of global scope initialization.
let dataOfClicks = [];
let startTime;
let dataLi;
let recordedTime;
let recordingName;

function timeNkey(tile) {
    const time = Date.now() - startTime;
    const key = tile.id;
    const json = {
        'time': time,
        'key': key
    }
    dataOfClicks.push(json);
}

function record() {
    recording = true;
    recBtn.classList.add('recording');
    recBtn.innerText = 'Recording...';
    dataLi = document.querySelector('#dataCont li');
    startTime = Date.now();
    dataLi.id = startTime;
    showTimeOfRecording(startTime, dataLi);
    for (const tile of pianoTiles) {
        tile.addEventListener('pointerdown', () => timeNkey(tile));
        tile.addEventListener('pointerup', () => timeNkey(tile));
    }
    recBtn.addEventListener("click", () => stopRecording(dataLi), { once: true });
}

function preview() {
    console.log(JSON.stringify(dataOfClicks, null, 1));
}

const recBtn = document.querySelector("#rec");
recBtn.addEventListener("click", record, { once: true });

const jsonBtn = document.querySelector("#jsonPrev");
/*jsonBtn.addEventListener("click", preview);*/

let recording = false;

function showTimeOfRecording(time, dataLi) {
    if (recording) {
        const newTime = Date.now();
        let realTime = newTime - time;
        recordedTime = realTime;
        dataLi.innerText = `Recording for ${(realTime / 1000).toFixed(1)} seconds.`;
        setTimeout(() => showTimeOfRecording(time, dataLi), 223);
    }
}

function stopRecording() {
    recordingName = prompt("Please enter a name for the recording:", "enter name");

    if (recordingName !== null && recordingName !== "") {
        console.log("Recording name saved:", recordingName);
    } else {
        recordingName = "My Recording";
    }

    saveData();
    recBtn.addEventListener("click", record, { once: true });
    recording = false;
    recBtn.classList.remove('recording');
    recBtn.innerText = 'Record';
    dataLi.innerText = `Recording saved. Duration - ${(recordedTime / 1000).toFixed(2)} seconds.`
}

function saveData() {
    // First, create an object with the name and clicks keys
    console.log(dataOfClicks);
    const recordingData = {
        "name": recordingName, // Set the recording name as desired
        "clicks": dataOfClicks // data
    };
    console.log(recordingData);

    // Then, proceed with the fetch request, sending recordingData as the body
    fetch("https://onkrajreda.onrender.com/saveRecording", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(recordingData) // Convert the recordingData object into a JSON string
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse JSON response body
    })
    .then(data => {
        console.log(data); // Handle success
    })
    .catch(error => {
        console.error('Error:', error); // Handle errors, such as network issues
    });
    fetchRecordings();
    // clear dataOfClicks
    dataOfClicks = [];
}

function fetchRecordings() {
    fetch("https://onkrajreda.onrender.com/list-recordings")
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('recordingsTable').getElementsByTagName('tbody')[0];
            tbody.innerHTML = ''; // Clear existing rows
            data.forEach(recording => {
                const row = tbody.insertRow();
                row.insertCell().textContent = recording.id;
                row.insertCell().textContent = recording.name;
                const playCell = row.insertCell();
                const playButton = document.createElement('button');
                playButton.textContent = 'Play';
                playButton.onclick = () => playRecording(recording.id, recording.data);
                playCell.appendChild(playButton);

                const renameCell = row.insertCell();
                const renameButton = document.createElement('button');
                renameButton.textContent = 'Rename';
                renameButton.onclick = () => renameRecording(recording.id);
                renameCell.appendChild(renameButton);

                const deleteCell = row.insertCell();
                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Delete';
                deleteButton.onclick = () => deleteRecording(recording.id);
                deleteCell.appendChild(deleteButton);
            });
        });
}

function renameRecording(id) {
    const newName = prompt('Enter new name:');
    if (newName) {
        fetch('https://onkrajreda.onrender.com/rename-recording', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id, newName }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                fetchRecordings(); // Refresh the table
            } else {
                alert('Rename failed');
            }
        });
    }
}

function deleteRecording(id) {
    if (confirm('Are you sure you want to delete this recording?')) {
        fetch('https://onkrajreda.onrender.com/delete-recording', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                fetchRecordings(); // Refresh the table
            } else {
                alert('Delete failed');
            }
        });
    }
}


function startNoteAutoplay(key) {
    const note = key;
    const pitch = notesFreq.get(note);
    const tile = document.querySelector(`#${key}`);
    tile.classList.add('active');

    // Stop any existing note for this key
    if (activeOscillators.has(note)) {
        const existing = activeOscillators.get(note);
        existing.oscillator.stop();
        existing.oscillator.disconnect();
        existing.gainNode.disconnect();
    }

    const { oscillator, gainNode } = createOscillatorAndGainNode(pitch);
    oscillator.start();
    const noteEventId = Date.now();
    activeOscillators.set(note, { oscillator, gainNode, noteEventId });
}

function stopNoteAutoplay(key) {
    const note = key;
    const tile = document.querySelector(`#${key}`);
    tile.classList.remove('active');
    const releaseTime = audioContext.currentTime;
    const { oscillator, gainNode, noteEventId } = activeOscillators.get(note);
    const decayDuration = 2;
    gainNode.gain.cancelScheduledValues(releaseTime);
    gainNode.gain.setValueAtTime(gainNode.gain.value, releaseTime); // New line to set current gain
    gainNode.gain.exponentialRampToValueAtTime(0.001, releaseTime + decayDuration);
    setTimeout(() => {
        // Check if the current note event is still the one that should be stopped
        if (activeOscillators.has(note) && activeOscillators.get(note).noteEventId === noteEventId) {
            oscillator.stop();
            oscillator.disconnect();
            gainNode.disconnect();
            activeOscillators.delete(note);
        }
    }, decayDuration * 1000);
}

 /*[{"time": 878, "key": "E4"}, {"time": 984, "key": "E4"}, {"time": 1516, "key": "E4"}, {"time": 1609, "key": "E4"},
 {"time": 2179, "key": "F4"}, {"time": 2279, "key": "F4"}, {"time": 2765, "key": "F4"}, {"time": 2869, "key": "F4"},
 {"time": 3405, "key": "A4"}, {"time": 3479, "key": "A4"}, {"time": 4019, "key": "A4"}, {"time": 4085, "key": "A4"},
 {"time": 4656, "key": "G4"}, {"time": 4735, "key": "G4"}]
  */


function playRecording(id, jsonData) {
    console.log('Playing recording:', id, 'data: ', jsonData);
    const data = JSON.parse(jsonData);
    data.forEach(({time, key}) => {
        console.log(`key - ${key}, time - ${time}ms`);
        setTimeout(function () {
            if(!activeOscillators.has(key)) {
                startNoteAutoplay(key); // Start the note if not already playing
            } else {
                stopNoteAutoplay(key); // Stop the note if it is playing
            }
        }, time);
    });
}

fetchRecordings();