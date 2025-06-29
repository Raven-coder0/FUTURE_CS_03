# 🔐 Secure File Sharing System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Framework-Flask-lightgreen)
![License](https://img.shields.io/badge/License-MIT-informational)
![Security](https://img.shields.io/badge/Encryption-AES128-orange)

A secure web-based file sharing platform built using **Python Flask** and **AES encryption**. This project is part of the **Cyber Security Task 3** of the **Future Interns Internship Program**.

It allows users to:
- 📤 Upload files securely (AES-encrypted at rest)
- 📥 Download files (on-the-fly AES decryption)
- 🔐 Ensure file integrity and safe key management

---

## 📁 Project Structure

```
securefileshare/
│
├── app.py                # Main Flask application
├── templates/
│   └── index.html        # Frontend UI (Bootstrap 5)
├── uploads/              # Stores encrypted files
├── decrypted/            # Temporarily stores decrypted files
├── keys/                 # Stores encryption keys
├── venv/                 # Python virtual environment
└── README.md             # You’re here!
```

---

## 🚀 Features

✅ AES-128 CBC encryption for all uploaded files  
✅ Clean and modern responsive UI (Bootstrap 5)  
✅ Automatic decryption & download  
✅ Auto-deletes decrypted copies after serving  
✅ Flash messaging for secure feedback  
✅ Secure key storage in `.key` files  
✅ File validation with `secure_filename()`  

---

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/securefileshare.git
cd securefileshare
```

### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
```

### 3. Install dependencies

```bash
pip install flask pycryptodome
```

---

## 🧪 Run the App

```bash
python app.py
```

Visit in browser: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🔐 Encryption & Security

* Uses **AES-128 CBC** mode for encryption  
* Each file gets a **unique random key and IV**  
* Encrypted files stored in `uploads/`  
* Keys stored separately in `keys/`  
* Decrypted files are temporarily placed in `decrypted/` and removed after download  
* Uses Flask's `secure_filename()` to sanitize file names  
* UI is protected from XSS and file overwrite risks  

See more in `security_overview.md`

---



## 📄 License

Licensed under the [MIT License](LICENSE).

---

## 🙋‍♂️ Author

**Jagadeesh Kommineni**  
Cybersecurity Intern – Future Interns  
🔗 [LinkedIn](https://www.linkedin.com/in/yourprofile)
