import streamlit as st
from dateutil import parser as date_parser
from nltk.tokenize import word_tokenize
import re
from datetime import datetime, timedelta

def extract_reminders(notes_text):
    reminders = []
    keywords = ["deadline", "meeting", "submission", "training", "expense"]
    
    for i, note in enumerate(notes_text.split('\n\n')):
        for sentence in note.split('.'):
            tokens = word_tokenize(sentence.lower())
            for keyword in keywords:
                if keyword in tokens:
                    date, time = extract_datetime(sentence)
                    reminders.append({"note": f"Note {i+1}", "event": keyword, "date": date, "time": time, "text": sentence})
    
    return reminders

def extract_datetime(text):
    # Extract date
    date = extract_date(text)
    
    # Extract time
    time = extract_time(text)
    
    return date, time

def extract_date(text):
    try:
        # Extract day names using regular expression
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for day in days:
            if day in text.lower():
                return next_day_of_week(day).strftime('%Y-%m-%d')
        
        # If no day names found, parse using dateutil
        date = date_parser.parse(text, fuzzy_with_tokens=True)[0]
        return date.strftime('%Y-%m-%d')
    except ValueError:
        return None

def extract_time(text):
    try:
        time_regex = re.compile(r'\d{1,2}:\d{2}([ap]m)?')
        time_match = time_regex.search(text)
        if time_match:
            return time_match.group()
        else:
            return None
    except ValueError:
        return None

def next_day_of_week(day):
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    today = datetime.now()
    days_ahead = today.weekday() - days.index(day.lower())
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return today + timedelta(days=days_ahead)

# Function to process text file
def process_text_file(file_path):
    with open(file_path, 'r') as file:
        notes_text = file.read()
        reminders = extract_reminders(notes_text)
        if reminders:
            for reminder in reminders:
                st.write(f"Reminder from {reminder['note']}:")
                st.write(f"Event: {reminder['event']}")
                st.write(f"Date: {reminder['date']}")
                st.write(f"Time: {reminder['time']}")
                st.write(f"Text: {reminder['text']}\n")
        else:
            st.write("No reminders found")

# Streamlit app
def main():
    st.title("Text Reminder Extractor")
    st.write("Database file: notes.txt")
    process_text_file("notes.txt")


if __name__ == "__main__":
    main()
