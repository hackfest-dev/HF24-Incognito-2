import streamlit as st
from pytube import YouTube
import os
import sys
import time
import requests
from zipfile import ZipFile

st.markdown('# 📝 **Transcriber App**')
bar = st.progress(0)

# 2. Retrieving audio file from YouTube video
def get_yt(URL):
    video = YouTube(URL)
    yt = video.streams.get_audio_only()
    yt.download()

    #st.info('2. Audio file has been retrieved from YouTube video')
    bar.progress(10)