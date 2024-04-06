from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.wavpack import WavPack
from mutagen.oggvorbis import OggVorbis
import wave
import soundfile as sf
import re
import language_tool_python

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
