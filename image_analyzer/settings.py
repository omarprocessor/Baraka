"""
Django settings for image_analyzer project.
"""

from pathlib import Path
from decouple import config
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 Security - TEMPORARY FIX: Allow all hosts
SECRET_KEY = config('SECRET_KEY', default='unsafe-key')
DEBUG = config('DEBUG', default=True, cast=bool)  # Set to True temporarily

# 🆕 EMERGENCY FIX: Allow all hosts temporarily
ALLOWED_HOSTS = ['*']  # This will allow any host

# 🔌 Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'images',
]

# 🧱 Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'image_analyzer.urls'

# 🎨 Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'image_analyzer.wsgi.application'

# 🗄️ Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 🔑 Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🌍 Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 📦 Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 🖼️ Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 🧠 OpenAI API Key
OPENAI_API_KEY = config('OPENAI_API_KEY', default='')

# 🌐 CORS settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# ⚙️ REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.JSONParser',
    ],
}

# ✅ Default primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 🆕 Ensure media directory exists
try:
    os.makedirs(MEDIA_ROOT, exist_ok=True)
    os.makedirs(MEDIA_ROOT / 'images', exist_ok=True)
    print("✅ Media directories verified in settings")
except Exception as e:
    print(f"⚠️  Media directory warning: {e}")
