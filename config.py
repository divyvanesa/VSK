import os

# Base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Secret key for session management
SECRET_KEY = 'vsk-gujarat-secret-key-2023'

# Admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'

# Upload configuration
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Allowed file extensions
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mov', 'avi', 'webm'}
ALLOWED_DOCUMENT_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}