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

if text_files:
    text_file_names = [file.name for file in text_files]
    text_content = "\n".join([file.getvalue().decode("utf-8") for file in text_files])
    st.session_state["text_extract"] = text_content
prompt_template = """
    Welcome to the Notes QA Assistant!

You can interact with me in various ways to get assistance with your notes. Here are some suggestions to get started:

1. *Question Answering (QA)*:
    - Ask me anything related to the content of your notes, and I'll do my best to provide you with accurate answers.

2. *Summarization*:
    - Request a summary of your notes by using the function "summarize [filename]".

3. *Translation*:
    - Translate text to different languages using the function "translate [language code] [text_extract]".

4. *Text Analysis*:
    - Analyze your notes for keywords, key phrases, sentiment, or any other specific analysis you need.

5. *Content Generation*:
    - Generate new content based on your notes, such as creating outlines, essay drafts, or additional insights.

6. *Custom Operations*:
    - Specify a custom operation to perform on the content of your notes. Use the function "custom [operation] [filename]" to execute the operation.

7. *Content Specification*:
    - Specify your text content directly within your query. Start your query with "Content:" followed by your text content. For example, "Content: Lorem ipsum dolor sit amet..."

Feel free to explore and experiment with different interactions! If you have any specific requests or need assistance with something not listed here, just let me know, and I'll do my best to assist you.

Let's get started!
    Reply "Not applicable" if text is irrelevant.
     
    The text content is:
    {text_extract}
"""
prompt = st.session_state.get("prompt", [{"role": "system", "content": "none"}])

# Display previous chat messages
for message in prompt:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])
uestion = st.chat_input("Ask me anything to get started")

welcome_message = """
    Welcome to the Virtual Assistant!
    
     Hello there! I'm RogieAI your Virtual Assistant, ready to assist you. 
    Feel free to ask me anything, and I'll do my best to provide you with the information you need. 
"""

# Display the welcome message
with st.chat_message("assistant"):
    st.write(welcome_message)
# Handle the user's question
if question:
    text_extract = st.session_state.get("text_extract", None)
    if not text_extract:
        with st.message("assistant"):
            st.write("You need to provide a text file")
            st.stop()

    # Update the prompt with the text extract
    prompt[0] = {
        "role": "system",
        "content": prompt_template.format(text_extract=text_extract),
    }

    # Add the user's question to the prompt and display it
    prompt.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    # Display an empty assistant message while waiting for the response
    with st.chat_message("assistant"):
        botmsg = st.empty()

    # Call OpenAI's ChatGPT and display the response as it comes
    response = []
    result = ""
    for chunk in openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=prompt, stream=True
    ):
        text = chunk.choices[0].get("delta", {}).get("content")
        if text is not None:
            response.append(text)
            result = "".join(response).strip()
            botmsg.write(result)

    # Add the assistant's response to the prompt
    prompt.append({"role": "assistant", "content": result})

    # Store the updated prompt in the session state
    st.session_state["prompt"] = prompt
