import streamlit as st
from pytube import YouTube
import os
import sys
import time
import requests
from zipfile import ZipFile

st.markdown('# 📝 **Transcriber App**')
bar = st.progress(0)