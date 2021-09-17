import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
BP_IMAGES_STORAGE = '/application/src/bp_images'

CORS_ALLOWED_HOSTS = [
    'http://localhost:8080',
    'http://127.0.0.1:8080',
]
CORS_ALLOWED_METHODS = [
    '*'
]
CORS_ALLOWED_HEADERS = [
    '*'
]
CORS_ALLOW_CREDENTIALS = True
