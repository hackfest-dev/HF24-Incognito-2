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
