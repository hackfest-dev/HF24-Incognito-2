import streamlit as st
st.set_page_config(
    page_title="Multipage app",
    page_icon="😆"
)
st.title("Homepage")
st.sidebar.success("select the pages")
# Function to add a new note
def add_note():
    note = st.text_input("Enter your note:")
    if st.button("Add Note", key="add_note_button"):
        if note:
            with open("notes.txt", "a") as file:
                file.write(note + "\n")
            st.success("Note added successfully!")
        else:
            st.error("Please enter a note.")

# Function to view all notes
def view_notes():
    with open("notes.txt", "r") as file:
        notes = file.readlines()
    if notes:
        st.subheader("Your Notes:")
        for i, note in enumerate(notes):
            st.markdown(f'<p class="neon-text">{i+1}. {note.strip()}</p>', unsafe_allow_html=True)
    else:
        st.subheader("Your Notes:")
        st.write("No notes found.")

# Function to delete a note
def delete_note():
    with open("notes.txt", "r") as file:
        notes = file.readlines()
    if notes:
        options = [f"{i+1}. {note.strip()}" for i, note in enumerate(notes)]
        selected_option = st.selectbox("Select a note to delete:", options)
        if st.button("Delete Note", key="delete_note_button"):
            index = int(selected_option.split(".")[0]) - 1
            del notes[index]
            with open("notes.txt", "w") as file:
                file.writelines(notes)
            st.success("Note deleted successfully!")
    else:
        st.error("No notes found to delete.")

# Main function to run the Streamlit app
def main():
    st.title("Notes App")
    st.markdown('<link rel="stylesheet" type="text/css" href="styles.css">', unsafe_allow_html=True)  # Link CSS file

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
