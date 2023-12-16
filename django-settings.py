from pathlib import Path
import os

from django.contrib.messages import constants as messages
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = ''


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = ['http://localhost:3001', 'http://localhost:3000',"https://*","http://*",  "https://13.127.252.123","https://domain-name.com"]
CSRF_TRUSTED_ORIGINS = ['http://localhost:3001', 'http://localhost:3000',"https://*","http://*","https://13.127.252.123","https://domain-name.com"]
CORS_ORIGIN_WHITELIST = ['http://localhost:3000',"https://13.127.252.123","https://domain-name.com","*"]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEBUG = True
ALLOWED_HOSTS = ['*']
# Application definition
INSTALLED_APPS = [
    'rest_framework',
    'blog.apps.BlogConfig',
    'users.apps.UsersConfig',
    'crispy_forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'phone_field',
    'django_filters',
    'bootstrap_datepicker_plus',
    'django.contrib.humanize',
    'star_ratings',
    'django_agenda',
    'video_call_chats',
    'channels',
    'Company_Staff',
    'doctor',
    'carecenter',
    'rest_framework.authtoken',
    'knox',
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

ROOT_URLCONF = 'django_project.urls'
SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))
AUTH_USER_MODEL = 'users.CustomUser'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}
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

WSGI_APPLICATION = 'django_project.wsgi.application'
ASGI_APPLICATION = "django_project.asgi.application"
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

DATE_INPUT_FORMATS = ('%d-%m-%Y')
DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.postgresql_psycopg2",
        'NAME': "",
        'USER': "",
        'PASSWORD': "",
        'HOST': "cklui4w20rsw.ap-south-1.rds.amazonaws.com",
        'PORT': "5432",
    }
}
# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [

]
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = False

CORS_ALLOW_METHODS = [
'DELETE',
'GET',
'OPTIONS',
'PATCH',
'POST',
'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/profile_pics/'
CRISPY_TEMPLATE_PACK = 'bootstrap4'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'login'

#######################################
###############  E M A I L  ###########

EMAIL_BACKEND = 'django_ses.SESBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST = 'email-smtp.ap-south-1.amazonaws.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
AWS_SES_REGION_NAME = 'ap-south-1'
AWS_SES_REGION_ENDPOINT = 'email.ap-south-1.amazonaws.com'

MESSAGE_TAGS = {
    messages.ERROR:'danger'
}
STATIC_URL = '/staticfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/profile_pics/'

# Email backend settings for Django
EMAIL_BACKEND = 'django_ses.SESBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST = 'email-smtp.ap-south-1.amazonaws.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
AWS_SES_REGION_NAME = 'ap-south-1'
AWS_SES_REGION_ENDPOINT = 'email.ap-south-1.amazonaws.com'

# #Aws - Credential's
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_STORAGE_BUCKET_NAME= ''
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_QUERYSTRING_AUTH = False

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % "{s3-bucket-name}"
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
  
STATIC_URL = 'https://%s/%s/' % ('s3.ap-south-1.amazonaws.com/{s3-bucket-name}/staticfiles/', '')
