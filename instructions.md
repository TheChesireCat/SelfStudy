-- nov 4 2024 --
**TTS for the pdf reader**

using tts rocks js :

<!DOCTYPE html>
<html>
<head>
    <title>TTS Integration Example</title>
</head>
<body>
    <!-- Include the TTS library -->
    <script src="https://tts.rocks/tts.js"></script>
    
    <!-- Your content -->
    <textarea id="text">Hello, world!</textarea>
    <button onclick="speak()">Speak</button>
    
    <script>
        // Initialize TTS
        window.TTS = window.TTS || {};
        
        // Configure settings
        TTS.TTSProvider = 'kokoro'; // or 'kitten', 'piper', etc.
        TTS.rate = 1.0;  // Speech rate
        TTS.pitch = 1.0; // Voice pitch
        
        async function speak() {
            const text = document.getElementById('text').value;
            
            // For Kokoro TTS (requires initialization)
            if (TTS.TTSProvider === 'kokoro') {
                if (!TTS.kokoroLoaded) {
                    await TTS.initKokoro();
                }
                await TTS.kokoroTTS(text);
            } 
            // For simpler engines
            else {
                TTS.speak(text, true);
            }
        }
    </script>
</body>
</html>

what i need is to see if we can select text in the pdf viewer and have it read out loud using tts.rocks