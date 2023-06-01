from flask import Flask, request
import os
import openai

app = Flask(__name__)
openai.api_key = 'YOUR_OPEN_AI_KEY'

@app.route('/')
def index():
    return """
    <html>
        <body>
            <button onclick="startRecording()">Start Recording</button>
            <button onclick="stopRecording()">Stop Recording</button>
            <script>
                let rec;
                let audioChunks = [];
                
                function startRecording() {
                    audioChunks = [];
                    rec = new MediaRecorder(window.stream);
                    rec.ondataavailable = e => {
                        audioChunks.push(e.data);
                    };
                    rec.start();
                }

                function stopRecording() {
                    rec.stop();
                    const audioBlob = new Blob(audioChunks);
                    const reader = new FileReader();
                    reader.readAsDataURL(audioBlob);
                    reader.onloadend = () => {
                        const base64data = reader.result;
                        fetch('/transcribe', {
                            method: 'POST',
                            body: JSON.stringify({ data: base64data }),
                            headers: { 'Content-Type': 'application/json' }
                        }).then(response => response.text()).then(data => {
                            console.log(data);
                        });
                    };
                }
            </script>
        </body>
    </html>
    """

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    audio_data = request.json['data']
    # Here you need to convert the base64 audio data into a format suitable for the OpenAI API.
    # This will likely involve writing the data to a file, or converting it to the correct audio format.
    transcript = openai.Audio.transcribe("whisper-1", audio_data)
    return transcript
