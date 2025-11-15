import streamlit as st
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
from datetime import datetime
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Neo4j configuration
uri = os.getenv('NEO4J_URI')
user = os.getenv('NEO4J_USERNAME')
password = os.getenv('NEO4J_PASSWORD')

# Initialize Neo4j driver
try:
    driver = GraphDatabase.driver(uri, auth=(user, password))
except Exception as e:
    st.error(f"Error initializing Neo4j driver: {e}")
    driver = None

# Ensure 'files' directory exists
files_dir = 'files'
if not os.path.exists(files_dir):
    os.makedirs(files_dir)

def create_document(tx, file_name, file_type, upload_date, upload_time, uploader):
    query = (
        "CREATE (d:Document {file_name: $file_name, file_type: $file_type, upload_date: $upload_date, upload_time: $upload_time, uploader: $uploader}) "
        "RETURN d"
    )
    tx.run(query, file_name=file_name, file_type=file_type, upload_date=upload_date, upload_time=upload_time, uploader=uploader)

def list_documents(tx):
    query = "MATCH (d:Document) RETURN d.file_name AS file_name, d.file_type AS file_type, d.upload_date AS upload_date, d.upload_time AS upload_time, d.uploader AS uploader"
    result = tx.run(query)
    return [record.data() for record in result]

def delete_document(tx, file_name):
    query = "MATCH (d:Document {file_name: $file_name}) DETACH DELETE d"
    tx.run(query, file_name=file_name)

def log_action(tx, action, file_name, user, timestamp):
    query = (
        "CREATE (a:ActionLog {action: $action, file_name: $file_name, user: $user, timestamp: $timestamp}) "
        "RETURN a"
    )
    tx.run(query, action=action, file_name=file_name, user=user, timestamp=timestamp)

def get_action_history(tx):
    query = "MATCH (a:ActionLog) RETURN a.action AS action, a.file_name AS file_name, a.user AS user, a.timestamp AS timestamp ORDER BY a.timestamp DESC"
    result = tx.run(query)
    return [record.data() for record in result]

def upload_files(files, uploader):
    if driver is None:
        st.error("Neo4j driver is not initialized.")
        return
    for file in files:
        file_name = file.name
        file_type = file.type
        now = datetime.now()
        upload_date = now.date().isoformat()
        upload_time = now.time().isoformat()
        timestamp = now.isoformat()
        try:
            # Save file locally
            file_path = os.path.join(files_dir, file_name)
            with open(file_path, 'wb') as f:
                f.write(file.getvalue())
            
            # Store metadata in Neo4j
            with driver.session() as session:
                session.execute_write(create_document, file_name, file_type, upload_date, upload_time, uploader)
                session.execute_write(log_action, 'upload', file_name, uploader, timestamp)
            st.success(f'File metadata for "{file_name}" stored and file uploaded successfully!')
        except Exception as e:
            st.error(f"Error uploading file metadata for {file_name}: {e}")

def list_files():
    if driver is None:
        st.error("Neo4j driver is not initialized.")
        return []
    try:
        with driver.session() as session:
            documents = session.execute_read(list_documents)
        return documents
    except Exception as e:
        st.error(f"Error retrieving files: {e}")
        return []

def remove_file(file_name, user):
    if driver is None:
        st.error("Neo4j driver is not initialized.")
        return
    timestamp = datetime.now().isoformat()
    try:
        # Remove file from database
        with driver.session() as session:
            session.execute_write(delete_document, file_name)
            session.execute_write(log_action, 'delete', file_name, user, timestamp)
        
        # Remove file locally
        file_path = os.path.join(files_dir, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            st.success(f'File "{file_name}" removed successfully!')
        else:
            st.error(f"File '{file_name}' not found in local storage.")
    except Exception as e:
        st.error(f"Error removing file {file_name}: {e}")

def get_file(file_name):
    file_path = os.path.join(files_dir, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return f.read()
    else:
        st.error(f"File '{file_name}' not found.")
        return None

# Function to list action history
def list_action_history():
    if driver is None:
        st.error("Neo4j driver is not initialized.")
        return []
    try:
        with driver.session() as session:
            actions = session.execute_read(get_action_history)
        return actions
    except Exception as e:
        st.error(f"Error retrieving action history: {e}")
        return []

# Login credentials
users = {
    "Emuna": "Emuna@0911",
    "Gokul": "Krish@3009",
    "Madu": "1234",
    "Divia": "1234",
    "Admin": "1234"
}

# Streamlit UI
st.title('Cloud-Based Document Management System ')

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# Login functionality
if not st.session_state.logged_in:
    st.subheader('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f'Login successful! Welcome, {username}')
        else:
            st.error('Invalid username or password')

# Main application
if st.session_state.logged_in:
    menu = st.sidebar.selectbox('Menu', ['Upload Files', 'List Files', 'Remove File', 'Action History'])
    if st.sidebar.button('Logout'):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success('You have been logged out.')

    if menu == 'Upload Files':
        st.subheader('Upload Documents')
        st.write(f"Logged in as: {st.session_state.username}")
        files = st.file_uploader('Choose files', accept_multiple_files=True)
        if files:
            upload_files(files, st.session_state.username)

    elif menu == 'List Files':
        st.subheader('List of Documents')
        documents = list_files()
        if documents:
            df = pd.DataFrame(documents)
            df.index += 1
            df.reset_index(inplace=True)
            df.columns = ['S.No', 'File Name', 'File Type', 'Upload Date', 'Upload Time', 'Uploader']
            st.table(df)

            # Add download and view functionality
            selected_file = st.selectbox('Select a file to view or download', [doc['file_name'] for doc in documents])
            if selected_file:
                file_data = get_file(selected_file)
                if file_data:
                    st.download_button('Download', file_data, selected_file)
                    st.write(f"**File Name**: {selected_file}")
                    st.write(f"**File Type**: {next(doc['file_type'] for doc in documents if doc['file_name'] == selected_file)}")
                    st.write(f"**Upload Date**: {next(doc['upload_date'] for doc in documents if doc['file_name'] == selected_file)}")
                    st.write(f"**Upload Time**: {next(doc['upload_time'] for doc in documents if doc['file_name'] == selected_file)}")
                    st.write(f"**Uploader**: {next(doc['uploader'] for doc in documents if doc['file_name'] == selected_file)}")

    elif menu == 'Remove File':
        st.subheader('Remove Document')
        file_name_to_remove = st.text_input('Enter the file name to remove')
        if st.button('Remove File'):
            remove_file(file_name_to_remove, st.session_state.username)

    elif menu == 'Action History':
        st.subheader('Action History')
        actions = list_action_history()
        if actions:
            df = pd.DataFrame(actions)
            df.index += 1
            df.reset_index(inplace=True)
            df.columns = ['S.No', 'Action', 'File Name', 'User', 'Timestamp']
            st.table(df)
else:
    st.info("Please log in to access the document management system.")
