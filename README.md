# Backend for AI Chat Application

This repository contains the backend code for an AI chat application. The backend is built using FastAPI and is designed to handle chat requests from a frontend application. It includes functionality for verifying API requests, processing chat messages, and integrating with OpenAI's GPT model for generating responses.

## Features

- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- **CORS Middleware**: Configured to allow requests from any origin, with credentials, and all methods and headers.
- **API Key Verification**: Ensures that only authorized requests are processed.
- **File Upload Handling**: Supports optional file uploads with chat messages.
- **OpenAI Integration**: Uses OpenAI's model to generate responses based on the provided context.
- **ChromaDB Integration**: Utilizes ChromaDB for querying relevant documents to provide context for the AI responses.

## Project Structure
    backend/ 
    ├── api/ 
    │ ├── __init__.py 
    │ ├── app.py 
    │ ├── embedding.py 
    │ ├── rag.py 
    ├── .gitignore 
    ├── local.settings.json 
    ├── requirements.txt 
    ├── start.ps1 
    ├── vercel.json 
    └── README.md

- **api/**: Contains the main application code.
  - **app.py**: The main FastAPI application file.
  - **embedding.py**: Handles interactions with ChromaDB for document retrieval.
  - **rag.py**: Processes requests and generates responses using OpenAI's GPT model.
- **.gitignore**: Specifies files and directories to be ignored by Git.
- **local.settings.json**: Contains local environment variables for development.
- **requirements.txt**: Lists the Python dependencies required for the project.
- **start.ps1**: A PowerShell script to set up the environment and run the application locally.
- **vercel.json**: Configuration file for deploying the application on Vercel.
- **README.md**: This file.

## Getting Started

### Prerequisites

- Python 3.11+
- pip (Python package installer)

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/your-username/your-repository-name.git
   cd your-repository-name
   ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1  # On Windows
    # source .venv/bin/activate  # On macOS/Linux
    ```

3. Install the dependencies:
    ```
    pip install -r requirements.txt
    ```

4. Create a local.settings.json file with the following content:
    ```json
    { 
        "API_KEY": "your-api-key", 
        "OPENAI_API_KEY": "your-openai-api-key" 
    }
    ```

5. Run the application locally:
    ```sh
    .\start.ps1  # On Windows
    # uvicorn api.app:app --host 0.0.0.0 --port 9000 --reload  # On macOS/Linux
    ```