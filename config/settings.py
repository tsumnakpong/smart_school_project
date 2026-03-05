
from pathlib import Path
from django.conf import settings  # ต้องมีคำว่า .conf ด้วยนะครับ
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-85hx3qyy0&0&x=&mmu^e#h4vkx+bt&(z+-&38yzgqlcv8ru77!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.137.1', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'core',
    'islamic',
    'sms',
    'lms',
    'cms',
    'iot',
    'mis',
    
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cms.context_processors.menu_context',  # <-- เพิ่มบรรทัดนี้ครับ
                'islamic.context_processors.prayer_navbar_data',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
# 1. ตรวจสอบว่ารหัสผ่านคล้ายกับข้อมูลส่วนตัวไหม (UserAttributeSimilarityValidator)
    # { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },

    # 2. ตรวจสอบความยาวขั้นต่ำ (ขั้นต่ำปกติคือ 8 ตัว)
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 4,  # ปรับลดเหลือ 4 ตัวได้ตามใจชอบ
        }
    },

    # 3. ตรวจสอบว่าเป็นรหัสผ่านที่โหลเกินไปไหม (เช่น 123456, password)
    # { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },

    # 4. ตรวจสอบว่าเป็นตัวเลขล้วนๆ ไหม
    # { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'th'
TIME_ZONE = 'Asia/Bangkok'  # เปลี่ยนจาก UTC เป็น Asia/Bangkok
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'






# เพิ่มบรรทัดนี้ล่างสุดของไฟล์
AUTH_USER_MODEL = 'core.User'


# เมื่อ Login สำเร็จ ให้ไปที่หน้า Dashboard ของ LMS
# config/settings.py
LOGIN_REDIRECT_URL = 'dashboard_redirect' # ชื่อ name ที่จะตั้งในขั้นตอนถัดไป

# เมื่อ Logout ให้กลับไปหน้าแรก
LOGOUT_REDIRECT_URL = '/'

# หน้าสำหรับ Login (ในกรณีที่มีการใช้ @login_required แล้วยังไม่ได้เข้าสู่ระบบ)
LOGIN_URL = '/auth/login/'


GEMINI_API_KEY = "AIzaSyCr5EncveSvsmwF6kZ1NP_3RjoiMMP08jA"

# 1. URL สำหรับเรียกไฟล์ผ่าน Browser
STATIC_URL = 'static/'

# 2. โฟลเดอร์ที่เราเก็บไฟล์ไว้ตอนพัฒนา (ที่ครูเอาฟอนต์ไปวางไว้)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# settings.py
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-school-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your-app-password-16-digits' # รหัสผ่านแอปจาก Google

JAZZMIN_SETTINGS = {
    # ชื่อหัวข้อบน Browser Tab และหน้า Login
    "site_title": "Smart School Admin",
    "site_header": "Smart School Ecosystem",
    "site_brand": "Smart School",

    # Path ของโลโก้ (ชี้ไปที่โฟลเดอร์ static ของคุณ)
    # เช่น static/images/logo.png ให้ใส่แค่ "images/logo.png"
    "site_logo": "images/ST.png", 
    "login_logo": "images/ST.png",

    # ข้อความต้อนรับในหน้า Login
    "welcome_sign": "ยินดีต้อนรับสู่ระบบบริหารจัดการ Smart School",

    # ลิขสิทธิ์ที่ Footer
    "copyright": "Smart School Ecosystem 2026",

    # เมนูค้นหาโมเดล (Global Search)
    "search_model": ["auth.User", "sms.Student"],

    # รายละเอียดเมนูด้านข้าง (Side Menu)
    "topmenu_links": [
        {"name": "หน้าแรกเว็บ", "url": "home", "permissions": ["auth.view_user"]},
        {"model": "auth.User"},
    ],
    
    
    # แสดงไอคอนในเมนู
    "show_sidebar": True,
    "navigation_expanded": True,
    
    # ไอคอนสำหรับ App และ Model (ใช้ Font Awesome 6)
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "sms": "fas fa-school",
        "sms.student": "fas fa-user-graduate",
        "sms.teacher": "fas fa-chalkboard-teacher",
    },
    
    # ทำให้ UI เป็นแบบสวยงาม (เปลี่ยนสี Header/Footer)
    # "changeform_format": "horizontal_tabs",
    # "changeform_format": "vertical_tabs",
    #"changeform_format": "single",collapsible
    # กำหนดรูปแบบแยกตาม App และ Model
    "changeform_format": "single", 
    
    # หรือกำหนดแบบเจาะจงเฉพาะบาง Model
    "changeform_format_overrides": {
        "auth.user": "vertical_tabs",
        "cms.news": "collapsible",
    },
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary", # สีโลโก้ด้านซ้าย
    "accent": "accent-primary",
    "navbar": "navbar-dark navbar-primary", # สีแถบบน (สีน้ำเงิน)
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary", # สีเมนูด้านข้าง
    "sidebar_nav_small_text": False,
    # "sidebar_disable_expand": True, # ลองปิดการขยายเมนูอัตโนมัติ
    # "sidebar_nav_legacy_style": True, # ใช้สไตล์เมนูแบบเก่า (เสถียรกว่าในบาง Version)
    "sidebar_disable_expand": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default", # หรือลองเปลี่ยนเป็น "flatly", "default", "cerulean"
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}