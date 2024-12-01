from pathlib import Path

import loguru

# logger
LOGGER = loguru.logger
LOGGER.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="1 GB", compression='zip')

API_TOKEN = 'mnMZi5zK6pebtWOlQecKsAWsGFOKcFfZ'

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-7u)xr(_nyp2qv_^buqp&l$idc$u^9&!vu0yctrrdsvjia0yf5n'

DEBUG = True

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'jazzmin',
    'import_export',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # libs
    'strawberry',
    'corsheaders',

    # local apps
    'graphql_api.apps.GraphqlApiConfig',


]

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

ROOT_URLCONF = 'TON_market_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'TON_market_backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'toncoin_project_db',
        'USER': 'postgres',
        'PASSWORD': 'bebra2281!',
        'HOST': 'localhost',  
        'PORT': '5432',
    }
}

# cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'TON_market_graphql_client',
    },
    'redis': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/',  
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

CACHES['default'] = CACHES['redis']

CACHE_TTL = 60 * 60 * 24 * 7  # 1 week 

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  
]

CORS_ALLOW_ALL_ORIGINS = True


LANGUAGE_CODE = 'Ru-ru'

LANGUAGES = (
    ('en', 'English'),
    ('ru', 'Russian')
)

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


JAZZMIN_UI_TWEAKS = {
    "theme": "minty",
}

JAZZMIN_SETTINGS = {
    "site_title": "TON Market",

    "site_header": "TON Market",
    "site_brand": "TON Market",

    "topmenu_links": [
        {"name": "Операции с Базой Данных",  "url": "/functions_admin/" },
        {"name": "Таблицы",  "url": "/virtual_views/" },
    ],
}

