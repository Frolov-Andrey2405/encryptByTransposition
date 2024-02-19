"""
The code is a web application using Flask.
Provides a simple interface for encrypting and decrypting text
"""

import subprocess
import os
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


class Config:
    """
    This class holds configuration settings for the application
    """
    CHAR_POSITIONS_FILENAME = ""


app.config.from_object(Config)


@app.route("/")
def index():
    """
    It returns a rendered template,
    which is an HTML file created in the templates folder
    """
    return render_template("index.html")


@app.route("/run-script")
def run_script():
    """
    The run_script function runs the generator.py script,
    returns a 200 status code if successful, or 500 otherwise
    """
    try:
        subprocess.run(["python", "generator.py"], check=True)
        return "", 200
    except subprocess.CalledProcessError as e:
        print(f"Error running script: {e}")
        return "", 500


@app.route("/upload", methods=["POST"])
def upload():
    """
    The upload function is used to upload a file to the server.

    The uploaded file will be saved in the 'uploads' directory,
    its path will be stored in app.config['CHAR_POSITIONS_FILENAME']
    """
    if "file" not in request.files:
        return "No file part", 400

    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        return "No selected file", 400

    file_path = os.path.join("uploads", uploaded_file.filename)

    try:
        uploaded_file.save(file_path)
        app.config["CHAR_POSITIONS_FILENAME"] = file_path
        return "File uploaded successfully", 200
    except Exception as e:
        print(f"Error saving file: {e}")
        return "Error saving file", 500


def encrypt_word(input_value, char_positions, real_positions):
    """
    The encrypt_word function takes in a word,
    encrypts it using the char_positions dictionary.

    It returns an encrypted version of the input word.
    """
    encrypted_word = ""
    for char in input_value:
        if char in real_positions:
            char_index = real_positions[char] - 1
            encrypted_char = list(char_positions.keys())[char_index]
            encrypted_word += encrypted_char
        else:
            encrypted_word += char
    return encrypted_word


def generate_real_positions():
    """
    The generate_real_positions function returns a dictionary with the
    ASCII characters as keys and their positions in the ASCII table as values.
    """
    return {chr(i): i - 32 for i in range(33, 127)}


def read_character_positions(filename):
    """
    The read_character_positions function reads the first row of a file,
    returns a dictionary with the characters as keys,
    their positions in the row as values.
    """
    with open(filename, "r", encoding="utf-8") as file:
        content = file.readlines()

    first_row = content[0].strip().split()

    char_positions = {}
    for idx, char in enumerate(first_row, start=1):
        char_positions[char] = idx

    return char_positions


@app.route("/encrypt", methods=["POST"])
def encrypt():
    """
    The encrypt function takes a JSON object with the key 'text',
    returns a JSON object with the key 'result'.

    The value of result is an encrypted string.
    If no text is provided, it will return an error message.
    """
    data = request.json
    if "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    input_text = data["text"]
    char_positions = read_character_positions(
        app.config["CHAR_POSITIONS_FILENAME"])
    real_positions = generate_real_positions()
    encrypted_word = encrypt_word(input_text, char_positions, real_positions)

    return jsonify({"result": encrypted_word}), 200


def decrypt_word(encrypted_word, char_positions, real_positions):
    """
    The decrypt_word function takes an encrypted word,
    a dictionary of character positions and a dictionary of real positions
    """
    decrypted_word = ""
    word_buffer = ""

    def process_char(char):
        """
        The process_char function takes a single character as input,
        adds it to the word_buffer.

        If the character is in char_positions,
        then it will be decrypted using real_positions.

        If not, then the word buffer will be added to decrypted_word, cleared
        """
        nonlocal word_buffer, decrypted_word
        if char in char_positions:
            char_index = char_positions[char] - 1
            decrypted_char = list(real_positions.keys())[char_index]
            word_buffer += decrypted_char
        else:
            word_buffer += char
            if len(word_buffer) > 1:
                decrypted_word += word_buffer
            word_buffer = ""

    for char in encrypted_word:
        process_char(char)

    process_char("")

    return decrypted_word


@app.route("/decrypt", methods=["POST"])
def decrypt():
    """
    The decrypt function takes a JSON object with the key 'text',
    returns a JSON object with the key 'result'.

    The value of 'text' is decrypted using the character positions.
    The result is returned as the value of 'result'
    """
    data = request.json
    if "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    input_text = data["text"]
    char_positions = read_character_positions(
        app.config["CHAR_POSITIONS_FILENAME"])
    real_positions = generate_real_positions()
    decrypted_text = decrypt_word(input_text, char_positions, real_positions)

    return jsonify({"result": decrypted_text}), 200


if __name__ == "__main__":
    app.run(debug=False, port=5000)
