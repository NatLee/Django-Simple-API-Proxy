# Django Simple API Proxy

This is a simple tool for proxying any APIs easily on your Django server.

You can use it as middleware to make a layer for user authorization or something.

## Installation

```bash
pip install django-simple-api-proxy
```

## Quick Start

1. Add `django_simple_api_proxy` to your `INSTALLED_APPS` in `settings.py` like this:

```py
INSTALLED_APPS = [
...
'django_simple_api_proxy',
]
```

2. Add APP settings to your `settings.py` like this:

```py
TARGET_API_URL = 'https://httpbin.org'
PROXY_ROUTE_PATH = 'my_test_route'
PROXY_TARGET_PATH = ''
```

3. Include the `django_simple_api_proxy` URL settings in your project `urls.py` like this:

```py
from django.conf import settings
from django.urls import include
urlpatterns += [
    path(settings.PROXY_ROUTE_PATH, include('django_simple_api_proxy.urls'))
]
```

4. Test on your server.

```bash
python manage.py runserver
```

Here's an example you success proxy an API by visit the following URLs.

- http://127.0.0.1:8000/my_test_route/
- http://127.0.0.1:8000/my_test_route

And the result will be as below.

```log
[06/Sep/2022 01:26:04] "GET /my_test_route/ HTTP/1.1" 200 314
2022-09-06 01:26:06.338 | DEBUG    | django_simple_api_proxy.views:get:73 - ----- Proxy GET
2022-09-06 01:26:06.339 | DEBUG    | django_simple_api_proxy.views:get_proxy_path:37 - URL: /get
2022-09-06 01:26:06.340 | DEBUG    | django_simple_api_proxy.views:update_payload:49 - Username: #anonymous
```

```json
{
  "args": { "username": "#anonymous" },
  "headers": {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Host": "httpbin.org",
    "User-Agent": "python-requests/2.27.1",
    "X-Amzn-Trace-Id": "Root=1-6316360c-2308560261599de4071127ac"
  },
  "origin": "xxx.xxx.xxx.xxx",
  "url": "https://httpbin.org/get?username=%23anonymous"
}
```

But when you visit `http://127.0.0.1:8000/my_test_route/123`, you'll get error.

Cause this URL is not found on target API server.

So, this proxy server will return this for you.

```json
{ "status": "error" }
```

## Usage

After the quick start, you may want to change some methods with your API server like making an authorization.

You can do it with inheriting the `APIProxy` class.

Here is an example:

```py

import requests

from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from django_simple_api_proxy.views import APIProxy

class MyAPIProxy(APIProxy):
    # give custom authentication
    authentication_classes = [SessionAuthentication, JWTAuthentication]

    # give custom permission
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Get."""
        # your new `GET` logic here

        logger.debug("----- Proxy GET Heyyaya")
        response = {"status": "default error!!"}
        try:
            params = dict(request.GET)
            path = self.get_proxy_path(request)
            params = self.update_payload(request, params)
            middle_resp_ = self.send_request("GET", path, params=params)
            response = middle_resp_.json()
        except Exception as e:
            print('yooooo error occurs!!')
            print(e)
        return self.response(response)

```
