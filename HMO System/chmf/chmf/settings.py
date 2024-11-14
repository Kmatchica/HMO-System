"""
Django settings for chmf project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
import logging

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!91ztag@#k0$64jyht&b7=0l8v4^n!dg5r+n02)@#jiist(ijy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'login_app',
    'roles_app',
    'modulelist_app',
    'permission_app',
    'access_app',
    'provider_app',
    'specialization_app',
    'category_app',
    'doctor_app',
    'coopagent_app',
    'department_app',
    'userstatus_app',
    'providerstatus_app',
    'payablename_app',
    'providerdoctors_app',
    'doctorstatus_app',
    'medicalprocedures_app',
    'procedureprovider_app',
    'doctorroomfee_app',
    'roomtype_app',
    'natureofmembership_app',
    'MeansofFranchise_app',
    'Franchisestatus_app',
    'clientbranch_app',
    'saletype_app',
    'agentstatus_app',
    'franchise_app',
    
    'clientclassification_app',
    'clientstatus_app',
    'clientsob_app',
    'client_app',
    'sob_app',
    'memberstatus_app',
    'membergender_app',
    'member_app',
    'medicalavailmentstatus_app',
    'medicalavailmenttype_app',
    'medicalapprovalprocedure_app',
    'medicaldiagnosis_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'login_app.middleware.ErrorMiddleware',
]

ROOT_URLCONF = 'chmf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'chmf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'options': '-c search_path=users'},
        'NAME': 'employee.db',
        'USER':'postgres',
        'PASSWORD':'1CHMF2022',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Manila'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# This line of code has been added as it is needed to collect all static files.
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Folder for Global Static Files (css, js, boostrap):
STATICFILES_DIRS = [ BASE_DIR / 'globalstatic/'
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

##############################BACK END###############################
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'login_app.backends.CustomUserAuthBackend',
]
AUTH_USER_MODEL = 'login_app.User'
LOGIN_URL ='login'
LOGIN_REDIRECT_URL = 'login_app:login'
LOGOUT_REDIRECT_URL = 'login_app:login'

############################# Logging Configuration #############################

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django.log'),
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

##################setting
