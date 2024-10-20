import streamlit as st
import streamlit.components.v1 as components


def speechToText():
    st.title("Speech Recognition App")

    # Embed the HTML file content in Streamlit
    components.html("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Speech Recognition</title>
        </head>
        <body>
            <button id="start" onclick="startRecognition()">Start Recognition</button>
            <button id="end" onclick="stopRecognition()">Stop Recognition</button>
            <p id="output" style="color: white;"></p> <!-- Text color set to white -->

            <script>
                const output = document.getElementById('output');
                let recognition;
                let finalTranscript = ''; // Store the final transcript separately
                let isStopping = false;  // Track if the stop button was pressed

                function startRecognition() {
                    isStopping = false;  // Reset the stop flag
                    recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
                    recognition.lang = 'en-US';
                    recognition.continuous = true;
                    recognition.interimResults = true;

                    recognition.onstart = function() {
                        console.log('Recognition started');
                    };

                    recognition.onresult = function(event) {
                        let interimTranscript = ''; // Store interim transcript for each result

                        for (let i = event.resultIndex; i < event.results.length; ++i) {
                            if (event.results[i].isFinal) {
                                finalTranscript += event.results[i][0].transcript + ' '; // Append final transcript
                            } else {
                                interimTranscript += event.results[i][0].transcript + ' '; // Collect interim transcript
                            }
                        }

                        // Update the output with both final and interim transcripts
                        output.textContent = finalTranscript + interimTranscript;
                        console.log('Interim:', interimTranscript);
                        console.log('Final:', finalTranscript);
                    };

                    recognition.onerror = function(event) {
                        console.error('Recognition error:', event.error);
                    };

                    recognition.onend = function() {
                        if (!isStopping) {  // Only restart if the stop button wasn't pressed
                            console.log('Recognition ended, restarting...');
                            recognition.start(); // Restart recognition for continuous listening
                        }
                    };

                    recognition.start();
                    console.log('Recognition initiated');
                }

                function stopRecognition() {
                    isStopping = true;  // Set the stop flag to true
                    if (recognition) {
                        recognition.stop();
                        console.log('Recognition stopped');
                    }
                }
            </script>
        </body>
        </html>
        """, height=500)
