# Temporary File Host

Простой веб-сервис для загрузки и обмена файлами с ограничением по времени. Все файлы шифруются на сервере и автоматически удаляются после истечения срока.

## Особенности
- Шифрование AES-256 (Fernet)
- Ссылка действует от 1 до 720 часов
- Автоматическая очистка истёкших файлов
- Лёгкий интерфейс
- Не требует регистрации

## Запуск на сервере
```bash
git clone https://github.com/legenda189k-alt/temporary-file-host.git
cd temporary-file-host
pip install -r requirements.txt
python app.py