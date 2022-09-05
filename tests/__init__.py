import django
from django.conf import settings

settings.configure(
    DEBUG=True,
    USE_TZ=True,
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:"
        }
    },
    INSTALLED_APPS=[
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sites",
        "rest_framework",
        "django_simple_api_proxy",
    ],
    MIDDLEWARE_CLASSES=[
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ],
    ###################################
    ######### API PROXY SETTINGS #########
    ###################################

    TARGET_API_URL = 'https://httpbin.org',
    PROXY_ROUTE_PATH = 'my_test_route',
    PROXY_TARGET_PATH = 'get'

    ###################################
)

django.setup()
