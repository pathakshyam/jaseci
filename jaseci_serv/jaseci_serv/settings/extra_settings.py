"""
Django settings for jaseci project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os, sys

from .base import *

ADDITIONAL_APPS = [
    "rest_framework.authtoken",
    "dj_rest_auth",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "dj_rest_auth.registration",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.facebook",
    "allauth.socialaccount.providers.github",
    "allauth.socialaccount.providers.microsoft",
    "allauth.socialaccount.providers.okta",
    # "allauth.socialaccount.providers.openid",
    "jaseci_serv.jsx_oauth",
]

INSTALLED_APPS += ADDITIONAL_APPS


AUTH_PROVIDERS = {"facebook": "facebook", "google": "google", "email": "email"}

SOCIAL_AUTH_CREDS = {
    "google": {
        "GOOGLE_CLIENT_ID": os.environ.get("GOOGLE_CLIENT_ID"),
        "GOOGLE_CLIENT_SECRET": os.environ.get("GOOGLE_CLIENT_SECRET"),
    },
    "facebook": {
        "FACEBOOK_CLIENT_ID": os.environ.get("FACEBOOK_CLIENT_ID"),
        "FACEBOOK_CLIENT_SECRET": os.environ.get("FACEBOOK_CLIENT_SECRET"),
    },
}

JSX_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES[0]["DIRS"] += [os.path.join(JSX_DIR, "templates")]
KNOX_TOKEN_EXPIRY = 24


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_AUTH_TOKEN_MODEL = None

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"

SITE_ID = 1

DEFAULT_CALLBACK_URL_FOR_SSO = "/auth/examples/google/"
LICENSE_VALIDITY_PATH_URL = "http://localhost:9000/api/get_status/"
DEFAULT_LICENSE_ACCESS_KEY = "IDdb176b744badef34e1a63a36a8ad6b"
DEFAULT_LICENSE_SECRET_KEY = (
    "47c1187b0b22f8f3864007c21a46919d605e24a1035060d313591e88bbb6c60a"
)
LICENSE_VALIDATION_ERROR_MSG = (
    "Your license copy is invalid or expired. Please contact to Jaseci team."
)

SCHEDULER_CONFIG = {
    "apscheduler.jobstores.default": {
        "class": "django_apscheduler.jobstores:DjangoJobStore"
    },
    "apscheduler.executors.processpool": {"type": "threadpool"},
}

SCHEDULER_AUTOSTART = True

DEBUG = False
