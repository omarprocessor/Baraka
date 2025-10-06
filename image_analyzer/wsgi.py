"""
WSGI config for image_analyzer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'image_analyzer.settings')

# 🆕 CRITICAL: Create media directories before application starts
try:
    media_root = Path(__file__).resolve().parent.parent / 'media'
    images_dir = media_root / 'images'
    
    os.makedirs(media_root, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    
    print(f"✅ Media directories created successfully:")
    print(f"   - Media root: {media_root}")
    print(f"   - Images dir: {images_dir}")
except Exception as e:
    print(f"⚠️  Warning: Could not create media directories: {e}")

application = get_wsgi_application()