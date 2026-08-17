# Temporary File Host

Простой веб-сервис для загрузки и обмена файлами с ограничением по времени. Все файлы шифруются на сервере и автоматически удаляются после истечения срока.

## Особенности
- Шифрование AES-256 (Fernet)
- Ссылка действует от 1 до 720 часов
- Автоматическая очистка истёкших файлов
- Лёгкий интерфейс
- Не требует регистрации

- ⚠️ Limitations
- Max file size: 100 MB (configurable)
- TTL: 1–720 hours
- Storage: local disk (not S3/cloud)
- No password protection or download limits

## 🛡️ Security Note
- The encryption key is stored locally (`key.key`). For production, use environment variables or a secret manager.

## 📈 Roadmap
- Password-protected links
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

