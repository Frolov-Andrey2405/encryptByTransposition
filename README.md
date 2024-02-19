# Flask Text Encryption/Decryption Web App

This web application is built using Flask and provides a simple interface for encrypting and decrypting text. It uses a character substitution method based on pre-defined character positions.

## Features

- **Encryption**: Input a text, and the application will encrypt it using a character substitution algorithm.
- **Decryption**: Input an encrypted text, and the application will decrypt it back to the original text.
- **File Upload**: Upload a file containing character positions used for encryption and decryption.
- **Background Script Execution**: Run a background script (`generator.py`) to generate character positions.

## Usage

1. Start the application by running the `app.py` script.
```bash
python app.py
```

2. Access the application through your web browser at [http://localhost:5000](http://localhost:5000).

3. Use the provided interface to perform text encryption and decryption.

## Routes

- **GET /run-script**: Execute the `generator.py` script to generate character positions.
- **POST /upload**: Upload a file containing character positions for encryption and decryption.
- **POST /encrypt**: Encrypt a given text.
- **POST /decrypt**: Decrypt an encrypted text.

## How to Run the Script

### Prerequisites

- Python 3.x
- Flask

### Installation

Install the required Python packages using the following command:
```bash
pip install -r requirements.txt
```

### Running the Application

Run the application using the following command:
```bash
python app.py
```

## Note

- The application uses Flask as the web framework.
- Character positions for encryption and decryption are read from an uploaded file.
- The `generator.py` script is available for generating character positions.
- Ensure that the necessary dependencies are installed using the provided `requirements.txt` file.
