
# Cloud-Based Document Management System

A **Cloud-Based Document Management System** built with [Streamlit](https://streamlit.io/) and [Neo4j](https://neo4j.com/). This application enables users to upload, list, view, download, and remove documents while maintaining a comprehensive action history. It includes user authentication to ensure secure access.

## Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **User Authentication:** Secure login system with predefined users.
- **File Upload:** Upload multiple documents with metadata storage.
- **File Listing:** View a list of all uploaded documents with detailed information.
- **File Download:** Download documents and view their details.
- **File Removal:** Remove documents from both the database and local storage.
- **Action Logging:** Maintain a history of all actions (uploads and deletions).

## Demo

![Application Screenshot](screenshots/app_screenshot.png)

*Replace with actual screenshots of your application.*

## Installation

### Prerequisites

- **Python 3.7 or higher**
- **Neo4j Database**

### Clone the Repository

```bash
git clone https://github.com/your-username/cloud-document-management.git
cd cloud-document-management
```

### Creating the Environment

```bash
python -m venv venv
```

### Activating the Environment

For Windows:

```bash
venv\Scripts\activate
```

For macOS/Linux:

```bash
source venv/bin/activate
```

### Install the Requirements

```bash
pip install -r requirements.txt
```

## Configuration

### Neo4j Setup

1. **Install Neo4j:**
   If you haven't installed Neo4j, download it from the official website and follow the installation instructions.

2. **Start Neo4j:**
   Ensure that your Neo4j instance is running. By default, it runs on `bolt://localhost:7687`.

3. **Create a Database:**
   You can create a new database for this application or use the default one.

4. **Obtain Credentials:**
   Make sure you have the URI, username, and password for your Neo4j database.

### Environment Variables

Create a `.env` file in the root directory of the project to store your environment variables securely. Add the following variables to the `.env` file:

```plaintext
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=your_username
NEO4J_PASSWORD=your_password
```

### Run the Application

```bash
streamlit run app.py
```

## Application Features

1. **Upload Files:**
   - Navigate to the "Upload Files" section.
   - Select one or multiple files to upload.
   - The files will be saved locally in the `files` directory, and metadata will be stored in Neo4j.

2. **List Files:**
   - View all uploaded documents with details like file name, type, upload date, time, and uploader.
   - Select a file to download or view its details.

3. **Remove File:**
   - Enter the name of the file you wish to remove.
   - The file will be deleted from both local storage and the Neo4j database.

4. **Action History:**
   - View a log of all upload and delete actions performed within the system.

## Project Structure

```
cloud-document-management/
├── files/                  # Directory to store uploaded files
├── screenshots/            # Directory for screenshots (optional)
├── .env                    # Environment variables
├── .gitignore              # Git ignore file
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## Technologies Used

- **Streamlit:** For building the web application interface.
- **Neo4j:** Graph database for storing document metadata and action logs.
- **Python-dotenv:** For managing environment variables.
- **Pandas:** For data manipulation and display.

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**
2. **Create a New Branch**

```bash
git checkout -b feature/YourFeature
```

3. **Commit Your Changes**

```bash
git commit -m "Add some feature"
```

4. **Push to the Branch**

```bash
git push origin feature/YourFeature
```

5. **Open a Pull Request**

Please ensure that your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License.

## Contact

For any questions or suggestions, please open an issue or contact [gk5139272@gmail.com](mailto:gk5139272@gmail.com).
