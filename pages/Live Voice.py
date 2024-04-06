import assemblyai as aai
import pyaudio
import wave
import threading
import time
import nltk
import streamlit as st

def record_audio(filename):
    global recording
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
    st.text("Recording stopped.")

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

def speech_to_text(url, speaker_label, para_label, start_milliseconds, end_milliseconds):
    try:
        config = aai.TranscriptionConfig(auto_highlights=True,speaker_labels=speaker_label, audio_start_from=start_milliseconds, audio_end_at=end_milliseconds)
        transcriber = aai.Transcriber(config=config)
        transcript = transcriber.transcribe(url)

        if transcript.status == aai.TranscriptStatus.error:
            st.error(transcript.error)
            return ""
        else:
            formatted_transcript = ""  
            highlights=""
            
            for result in transcript.auto_highlights.results:
                highlights+= f"Highlight: {result.text}, Count: {result.count}, Rank: {result.rank}, Timestamps: {result.timestamps}\n"
                
            if speaker_label:
                speakers = set(utterance.speaker for utterance in transcript.utterances)
                if len(speakers) == 1:
                    if para_label:
                        paragraphs = transcript.get_paragraphs()
                        for paragraph in paragraphs:
                            formatted_transcript += paragraph.text + "\n"
                    else:
                        sentences = transcript.get_sentences()
                        for sentence in sentences:
                            formatted_transcript += sentence.text + "\n"
                else:
                    for utterance in transcript.utterances:
                        formatted_transcript += f"Speaker {utterance.speaker}: "
                        sentences = nltk.sent_tokenize(utterance.text)
                        if para_label:
                            paragraphs = [' '.join(sentences[i:i+2]) for i in range(0, len(sentences), 2)]
                            for paragraph in paragraphs:
                                formatted_transcript += paragraph + "\n"
                        else:
                            for sentence in sentences:
                                formatted_transcript += sentence + "\n"
            else:
                if para_label:
                    paragraphs = transcript.get_paragraphs()
                    for paragraph in paragraphs:
                        formatted_transcript += paragraph.text + "\n"  
                else:
                    sentences = transcript.get_sentences
            return formatted_transcript
    except Exception as e:
        st.error(f"An error occurred during transcription: {e}")
        return ""