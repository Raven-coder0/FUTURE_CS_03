from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from flask import after_this_request
import os
import time

app = Flask(__name__)
app.secret_key = os.urandom(16)

UPLOAD_FOLDER = 'uploads'
DECRYPT_FOLDER = 'decrypted'
KEY_FOLDER = 'keys'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'jpg', 'png', 'docx'}

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DECRYPT_FOLDER, exist_ok=True)
os.makedirs(KEY_FOLDER, exist_ok=True)

# AES encryption
BLOCK_SIZE = 16

def pad(data):
    pad_len = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([pad_len]) * pad_len

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    if uploaded_file and allowed_file(uploaded_file.filename):
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        data = uploaded_file.read()
        key = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(data))

        with open(file_path, 'wb') as f:
            f.write(cipher.iv + ciphertext)

        with open(os.path.join(KEY_FOLDER, filename + '.key'), 'wb') as kf:
            kf.write(key)

        flash('File uploaded and encrypted successfully!', 'success')
    else:
        flash('Invalid file type.', 'danger')
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    key_path = os.path.join(KEY_FOLDER, filename + '.key')
    temp_path = os.path.join(DECRYPT_FOLDER, filename)

    try:
        with open(file_path, 'rb') as f:
            iv = f.read(16)
            ciphertext = f.read()

        with open(key_path, 'rb') as kf:
            key = kf.read()

        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext))

        with open(temp_path, 'wb') as temp:
            temp.write(plaintext)

        @after_this_request
        def cleanup(response):
            try:
                os.remove(temp_path)
            except Exception as e:
                print(f"Failed to delete temp file: {e}")
            return response

        return send_file(temp_path, as_attachment=True)

    except Exception as e:
        flash(f"Error during download: {e}", 'danger')
        return redirect(url_for('index'))

    try:
        with open(file_path, 'rb') as f:
            iv = f.read(16)
            ciphertext = f.read()

        with open(key_path, 'rb') as kf:
            key = kf.read()

        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext))

        with open(temp_path, 'wb') as temp:
            temp.write(plaintext)

        return send_file(temp_path, as_attachment=True)

    finally:
        # Optional: wait a few seconds before auto-deletion
        time.sleep(3)
        if os.path.exists(temp_path):
            os.remove(temp_path)

# Optional: clear key or upload folder on startup
# import shutil; shutil.rmtree(UPLOAD_FOLDER); os.makedirs(UPLOAD_FOLDER)

if __name__ == '__main__':
    app.run(debug=True)
