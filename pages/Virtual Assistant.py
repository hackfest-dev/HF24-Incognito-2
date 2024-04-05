import streamlit as st
import openai
from dotenv import load_dotenv
import os
load_dotenv()
# Set the title for the Streamlit app
st.title("Virtual Assistant ")


# Set up the OpenAI API key
openai.api_key = os.getenv("Openai_key")

# Upload text files using Streamlit's file uploader
text_files = st.file_uploader("Upload Text Files", type="txt", accept_multiple_files=True)