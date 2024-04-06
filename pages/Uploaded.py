import streamlit as st
import nltk
import assemblyai as aai
import os
import threading
import re
import language_tool_python
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.wavpack import WavPack
from mutagen.oggvorbis import OggVorbis
import wave
import soundfile as sf
import datetime
import librosa
import requests
from bs4 import BeautifulSoup
import re
import ast
import asyncio

def get_audio_duration(filename):
    if filename.endswith('.mp3'):
        audio = MP3(filename)
    elif filename.endswith('.flac'):
        audio = FLAC(filename)
    elif filename.endswith('.wv'):
        audio = WavPack(filename)
    elif filename.endswith('.ogg'):
        audio = OggVorbis(filename)
    elif filename.endswith('.wav'):
        with wave.open(filename, 'rb') as audio_file:
            frames = audio_file.getnframes()
            rate = audio_file.getframerate()
            duration_seconds = frames / float(rate)
        return duration_seconds
    else:
        raise ValueError("Unsupported audio format")

    duration_seconds = audio.info.length
    return duration_seconds

def format_duration(duration):
    hours = int(duration / 3600)
    minutes = int((duration % 3600) / 60)
    seconds = int(duration % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def format_date(text):
    date_pattern = r'\b(\d{1,2}) (\d{1,2}) (\d{2}|\d{4})\b'

    def replace_date(match):
        day = match.group(1)
        month = match.group(2)
        year = match.group(3)
        if len(year) == 2:
            year = "" + year
        return f"{day}-{month}-{year}"

    formatted_text = re.sub(date_pattern, replace_date, text)
    return formatted_text

def grammar_check(text, language='en-US'):
    if not text.strip():
        return "No text provided for grammar checking."
    
    tool = language_tool_python.LanguageTool(language)
    matches = tool.check(text)
    corrected_text = tool.correct(text)
    return corrected_text
def get_image_suggestions(highlights, num_images):
    num_images=num_images + 1
    try:
        # Extract top 5 highlights
        top_highlights = sorted(highlights, key=lambda x: x['Rank'], reverse=True)[:num_images]
        
        # Construct search query from top highlights
        search_query = " ".join([highlight['Highlight'] for highlight in top_highlights])
        search_url = f"https://www.google.com/search?q={search_query}&tbm=isch"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        response = requests.get(search_url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tags = soup.find_all('img', limit=num_images)
            img_urls = [img['src'] for img in img_tags if img['src'].startswith('http')]
            return img_urls
        else:
            print("Failed to fetch image suggestions.")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
def high(highlights):
    highlights_list = []
    pattern = r"Highlight: (.*?), Count: (\d+), Rank: ([\d.]+), Timestamps: \[Timestamp\(start=(\d+), end=(\d+)\)\]"
    matches = re.findall(pattern, highlights)
    
    for match in matches:
        highlight_dict = {
        "Highlight": match[0],
        "Count": int(match[1]),
        "Rank": float(match[2]),
        "Timestamps": [{"start": int(match[3]), "end": int(match[4])}]
        }
        highlights_list.append(highlight_dict)

    return highlights_list


async def speech_to_text_async(url, speaker_label, para_label, start_milliseconds, end_milliseconds):
    loop = asyncio.get_event_loop()
    
    def transcribe_threaded():
        config = aai.TranscriptionConfig(auto_highlights=True, speaker_labels=speaker_label, audio_start_from=start_milliseconds, audio_end_at=end_milliseconds)
        transcriber = aai.Transcriber(config=config)
        return transcriber.transcribe(url)
    
    transcript = await loop.run_in_executor(None, transcribe_threaded)

    if transcript.status == aai.TranscriptStatus.error:
        print(transcript.error)
        return "", ""

    formatted_transcript = ""
    highlights = ""

    for result in transcript.auto_highlights.results:
        highlights += f"Highlight: {result.text}, Count: {result.count}, Rank: {result.rank}, Timestamps: {result.timestamps}\n"

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
            sentences = transcript.get_sentences()
            for sentence in sentences:
                formatted_transcript += sentence.text + "\n"

    return formatted_transcript, highlights


async def main_async():
    st.title("Speech-to-text")

    uploaded_file = st.file_uploader("Upload Audio File", type=["wav", "mp3", "flac", "ogg","mp4"])

    if uploaded_file:
        st.audio(uploaded_file, format='audio/ogg', start_time=0)
        
        audio_data, samplerate = librosa.load(uploaded_file, sr=44100)

        duration = len(audio_data) / samplerate
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        seconds = int(duration % 60)
        duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        st.write(f"Duration: {duration_str}")

        output_file = "output.wav"

        sf.write(output_file, audio_data, samplerate)

        #portion of text
        if st.checkbox("Do you want to transcribe portion of your file?"):
            st.write(f"Duration: {duration_str}")

        # Create sliders for start and end time
            st.subheader("Start Time")
            if hours:
                shours = st.slider("Hours", 0, hours, value=0)
            else:
                shours=0
            if minutes:
                sminutes = st.slider("Minutes", 0, 59, value=0)
            else:
                sminutes=0
            sseconds = st.slider("Seconds", 0, 59, value=0)

            st.subheader("End Time")
            if hours:
                ehours = st.slider("Hours", shours, hours, value=hours)
            else:
                ehours=0
            if minutes:
                eminutes = st.slider("Minutes", sminutes, 59, value=minutes)
            else:
                eminutes=0
            esseconds = st.slider("Seconds", sseconds, 59, value=seconds)
            
            start_milliseconds = (shours * 60 * 60 * 1000) + (sminutes * 60 * 1000) + (sseconds * 1000)
            end_milliseconds = (ehours * 60 * 60 * 1000) + (eminutes * 60 * 1000) + (esseconds * 1000)

        else:
            start_hours,start_minutes,start_seconds=0,0,0
            end_hours,end_minutes,end_seconds=map(int, duration_str.split(':'))
            start_milliseconds = (start_hours * 60 * 60 * 1000) + (start_minutes * 60 * 1000) + (start_seconds * 1000)
            end_milliseconds = (end_hours * 60 * 60 * 1000) + (end_minutes * 60 * 1000) + (end_seconds * 1000)

        speaker_label = st.checkbox("Enable Speaker Labels")
        para_label = st.checkbox("Transcribe into Paragraphs (Uncheck for Sentences)")
    

        if st.button("Transcribe"):
            text, highlights = await speech_to_text_async(output_file, speaker_label, para_label, start_milliseconds, end_milliseconds)

            if text:
                corrected_text = grammar_check(text)
                #if speaker_label:
                    #colored=display_colored_transcript(corrected_text)
                    #st.subheader("Transcription")
                    #st.text(colored)
            #else:   
                st.subheader("Transcription")
                st.text(corrected_text)
            else:
                st.write('No Text found')
                
            highlight=high(highlights)
                
            num_images = st.number_input("Number of Image Suggestions", min_value=1, max_value=10, value=5)
            img_urls = get_image_suggestions(highlight, num_images)
            if img_urls:
                st.write("Image suggestions:")
                for i,img_url in enumerate(img_urls):
                    st.image(img_url, caption=f'Image Suggestion {i+1}')
                    #choice = st.radio("Do you want to add any of these images to your notes?", ("Yes", "No"),key=f"image_{i}")
                    #if choice == "Yes":
                        #folder_path = st.text_input("Enter the folder path to save the images:",key=f"folder_path_{i}")
                        #if folder_path:
                            #download_images(img_urls, folder_path)
                        #else:
                            #st.write("Invalid folder path. Images not downloaded.")
                    #else:
                        #st.write("No images added to notes.")
            else:
                st.write("No image suggestions found.")


    else:
        st.info("Please upload an audio file.")

if __name__ == "__main__":
    asyncio.run(main_async())

