import pyaudio
import numpy as np
import wave
import threading

# Global variable to control recording
recording = False

def record_audio(filename):
    global recording
    print("Recording started. Press 'Enter' to stop recording...")
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    audio_data = []  # Initialize audio data array

    # Start recording
    recording = True
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    while recording:
        # Record audio in chunks
        data = stream.read(CHUNK)
        audio_data.append(data)

    # Stop recording
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Recording stopped.")

    # Save the recorded audio to a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(audio_data))
    wf.close()

def start_recording(filename):
    global recording
    if not recording:
        recording = True
        threading.Thread(target=record_audio, args=(filename,), daemon=True).start()

def stop_recording():
    global recording
    recording = False
