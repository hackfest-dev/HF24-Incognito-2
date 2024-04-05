import streamlit as st
st.set_page_config(
    page_title="Multipage app",
    page_icon="😆"
)

st.sidebar.success("select the pages")
import os
import streamlit as st

# Function to add a new note
def add_note():
    note = st.text_input("Enter your note:")
    if st.button("Add Note", key="add_note_button"):
        if note:
            note_number = len(os.listdir("notes")) + 1
            note_filename = f"note_{note_number}.txt"
            with open(os.path.join("notes", note_filename), "w") as file:
                file.write(note)
            st.success("Note added successfully!")
        else:
            st.error("Please enter a note.")

# Function to view all notes
def view_notes():
    note_files = os.listdir("notes")
    if note_files:
        st.subheader("Your Notes:")
        for note_filename in note_files:
            with open(os.path.join("notes", note_filename), "r") as file:
                note_content = file.read()
            st.write(f"- {note_content}")
    else:
        st.subheader("Your Notes:")
        st.write("No notes found.")

# Function to delete a note
def delete_note():
    note_files = os.listdir("notes")
    if note_files:
        options = [note_filename for note_filename in note_files]
        selected_option = st.selectbox("Select a note to delete:", options)
        if st.button("Delete Note", key="delete_note_button"):
            os.remove(os.path.join("notes", selected_option))
            st.success("Note deleted successfully!")
    else:
        st.error("No notes found to delete.")

# Main function to run the Streamlit app
def main():
    st.title("Notes App")

    # Create notes directory if it doesn't exist
    if not os.path.exists("notes"):
        os.makedirs("notes")

    st.sidebar.header("Menu")
    menu_options = ["Add Note", "View Notes", "Delete Note"]
    choice = st.sidebar.selectbox("Select an option:", menu_options)

    if choice == "Add Note":
        st.header("Add Note")
        add_note()
    elif choice == "View Notes":
        st.header("View Notes")
        view_notes()
    elif choice == "Delete Note":
        st.header("Delete Note")
        delete_note()

# Run the Streamlit app
if __name__ == "__main__":
    main()
