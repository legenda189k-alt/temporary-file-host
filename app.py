import os
import uuid
import io
from datetime import datetime, timedelta
from flask import Flask, request, render_template, send_file, jsonify, url_for
from cryptography.fernet import Fernet
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

app = Flask(__name__)

# Настройки из .env или значения по умолчанию
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24))
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads/')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_FILE_SIZE_MB', 100)) * 1024 * 1024

# Создаём папку для загрузок
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Ключ шифрования (хранится в файле, можно перенести в .env при желании)
KEY_FILE = 'key.key'
if os.path.exists(KEY_FILE):
    with open(KEY_FILE, 'rb') as f:
        KEY = f.read()
else:
    KEY = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as f:
        f.write(KEY)

cipher = Fernet(KEY)

# Хранилище ссылок (в памяти, для продакшена лучше использовать SQLite/Redis)
links = {}

def clean_expired_links():
    now = datetime.now()
    expired = [link_id for link_id, data in links.items() if data['expire'] < now]
    for link_id in expired:
        try:
            os.remove(links[link_id]['path'])
        except:
            pass
        del links[link_id]

@app.before_request
def before_request():
    clean_expired_links()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'Файл не выбран'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Файл не выбран'}), 400
    
    expire_hours = int(request.form.get('expire', 24))
    if expire_hours < 1 or expire_hours > 720:
        expire_hours = 24
    
    original_name = secure_filename(file.filename)
    if not original_name:
        original_name = 'file'
    
    file_id = str(uuid.uuid4())
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file_id)
    
    data = file.read()
    encrypted_data = cipher.encrypt(data)
    
    with open(filepath, 'wb') as f:
        f.write(encrypted_data)
    
    link_id = str(uuid.uuid4())[:8]
    expire_time = datetime.now() + timedelta(hours=expire_hours)
    
    links[link_id] = {
        'path': filepath,
        'expire': expire_time,
        'original_name': original_name,
        'size': len(data)
    }
    
    download_url = url_for('download', link_id=link_id, _external=True)
    
    return jsonify({
        'success': True,
        'link': download_url,
        'expire': expire_time.isoformat(),
        'filename': original_name,
        'size': len(data)
    })

@app.route('/download/<link_id>')
def download(link_id):
    link = links.get(link_id)
    if not link:
        return render_template('error.html', error='Ссылка недействительна'), 404
    
    if datetime.now() > link['expire']:
        return render_template('error.html', error='Срок действия ссылки истёк'), 410
    
    try:
        with open(link['path'], 'rb') as f:
            encrypted_data = f.read()
        decrypted_data = cipher.decrypt(encrypted_data)
        return send_file(
            io.BytesIO(decrypted_data),
            as_attachment=True,
            download_name=link['original_name'],
            mimetype='application/octet-stream'
        )
    except Exception as e:
        return render_template('error.html', error=f'Ошибка: {str(e)}'), 500

@app.route('/info/<link_id>')
def info(link_id):
    link = links.get(link_id)
    if not link:
        return jsonify({'error': 'Ссылка не найдена'}), 404
    return jsonify({
        'filename': link['original_name'],
        'size': link['size'],
        'expire': link['expire'].isoformat(),
        'active': datetime.now() < link['expire']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)