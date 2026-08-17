
📁 Temporary File Host

A secure, self-destructing file sharing service with AES-256 encryption.

Upload any file, get a shareable link, and the file will automatically disappear after a set time or number of downloads. All files are encrypted on the server side using Fernet (AES-128 CBC + HMAC-SHA256) – so even the server admin cannot read your content without the key.

---

✨ Features

· 🔐 AES-256 encryption – every file is encrypted before saving.
· ⏳ Custom TTL – set a lifetime from 1 to 720 hours (up to 30 days).
· 🗑️ Auto-deletion – files are permanently removed after expiry.
· 📦 No registration – upload and share instantly.
· 🌐 REST API – simple endpoints for programmatic uploads (see below).
· 🐳 Docker support – run with a single command.
· 📄 Privacy-first – no IP logging, no user tracking (see PRIVACY.md).

---

🚀 Quick Start

Using Docker (recommended)

```bash
docker run -d -p 5000:5000 --name temp-file-host legenda189k/temporary-file-host
```

Then open http://localhost:5000 in your browser.

Manual installation

```bash
# Clone the repository
git clone https://github.com/legenda189k-alt/temporary-file-host.git
cd temporary-file-host

# Install dependencies
pip install -r requirements.txt

# Generate a secret key (if not exists)
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())" > key.key

# Run the app
python app.py
```

The server will start at http://localhost:5000.

---

📖 Usage

Web Interface

1. Click "Choose File" and select your file.
2. Set the expiration time (in hours).
3. Click "Upload".
4. Copy the generated link and share it.
5. The file will be deleted automatically after the TTL expires.

API Endpoints

Method Endpoint Description
POST /upload Upload a file. Form-data: file (binary), ttl (int, hours). Returns { "link": "/download/<id>" }.
GET /download/<id> Download the file (if still alive).
HEAD /download/<id> Check if file exists (returns 200 or 404).

Example with curl:

```bash
curl -F "file=@myphoto.jpg" -F "ttl=24" https://your-host.com/upload
```

---

⚠️ Limitations (current version)

Limit Value
Max file size 100 MB
TTL range 1 – 720 hours
Storage backend Local disk (uploads/)
Concurrent downloads Not limited
Password protection Not yet (see Roadmap)

---

🔐 Security Note

· The encryption key (key.key) is stored locally by default. For production, always use environment variables or a secret manager (e.g., HashiCorp Vault, AWS Secrets Manager).
· Files are encrypted before writing to disk, but metadata (filename, size, timestamp) is stored in plaintext.
· We never log IP addresses or user agents – see our Privacy Policy.

---

🗺️ Roadmap (planned)

☐ Password-protected downloads
☐ Download counter limit (e.g., max 5 downloads)
☐ Chunked upload for large files (>100 MB)
☐ Telegram bot integration
☐ S3 / cloud storage support
☐ Admin dashboard with analytics

---

📜 Legal

This project is provided as-is, without any warranty. Use at your own risk.
By using this service, you agree to our Terms of Service and Privacy Policy.

---

🤝 Contributing

Pull requests are welcome! Please read our Contributing Guidelines and Code of Conduct first.

---

📄 License

This project is licensed under the MIT License – see the LICENSE file for details.

---

🙏 Acknowledgements

· Fernet for symmetric encryption.
· Flask – the lightweight web framework.

---

Made with ❤️ by legenda189k-alt
- Download count limits
- Telegram bot integration
- Chunked upload for large files
- Admin dashboard

## 📜 Legal
See [PRIVACY.md](PRIVACY.md) and [TERMS.md](TERMS.md).


## Запуск на сервере
```bash
git clone https://github.com/legenda189k-alt/temporary-file-host.git
cd temporary-file-host
pip install -r requirements.txt
python app.py

