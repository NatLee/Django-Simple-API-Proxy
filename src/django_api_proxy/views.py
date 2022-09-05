import json
import re
from urllib.parse import urlparse
from loguru import logger
import requests

# Create your views here.

from django.http import JsonResponse
from django.conf import settings

#from rest_framework.authentication import SessionAuthentication
#from rest_framework_simplejwt.authentication import JWTAuthentication
#from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView


class APIProxy(APIView):
    """API proxy"""

    authentication_classes = [] # disable auth
    permission_classes = [] # disable permission

    target_api_url = settings.TARGET_API_URL
    proxy_route_path = settings.PROXY_ROUTE_PATH
    proxy_target_path = settings.PROXY_TARGET_PATH

    def parse_path(self, request):
        parsed_path = urlparse(request.get_full_path())
        path = parsed_path.path.rstrip("/")
        path = re.sub(self.proxy_route_path, self.proxy_target_path, path, 1)
        return path

    def get_proxy_path(self, request):
        path = self.parse_path(request)
        logger.debug(f"URL: {path}")
        return f"{self.target_api_url}{path}"

    def response(self, resp: dict):
        return JsonResponse(resp, safe=False, json_dumps_params={"ensure_ascii": False})

    def update_payload(self, request, params):
        username = request.user.username
        
        if not username:
            username = '#anonymous'
        
        logger.debug(f"Username: {username}")
        params.update(
            {"username": username}
        )
        return params

    def send_request(
        self, method, url, params=None, data=None, json=None, timeout=180, verify=True
    ):
        return requests.request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json,
            timeout=timeout,
            verify=verify,
        )

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Get."""
        logger.debug("----- Proxy GET")
        response = {"status": "error"}
        with logger.catch():
            params = dict(request.GET)
            path = self.get_proxy_path(request)
            params = self.update_payload(request, params)
            middle_resp_ = self.send_request("GET", path, params=params)
            response = middle_resp_.json()
        return self.response(response)

    def post(self, request, *args, **kwargs):
        """Post."""
        logger.debug("----- Proxy POST")
        response = {"status": "error"}
        with logger.catch():
            params = json.loads(request.body)
            logger.debug(f"JSON Params: {params}")
            path = self.get_proxy_path(request)
            params = self.update_payload(request, params)
            middle_resp_ = self.send_request("POST", path, json=params)
            response = middle_resp_.json()
        return self.response(response)

    def patch(self, request, *args, **kwargs):
        """Patch."""
        logger.debug("----- Proxy PATCH")
        response = {"status": "error"}
        with logger.catch():
            params = json.loads(request.body)
            logger.debug(f"JSON Params: {params}")
            path = self.get_proxy_path(request)
            params = self.update_payload(request, params)
            middle_resp_ = self.send_request("PATCH", path, json=params)
            response = middle_resp_.json()
        return self.response(response)

    def delete(self, request, *args, **kwargs):
        """Delete"""
        logger.debug("----- Proxy DELETE")
        response = {"status": "error"}
        with logger.catch():
            params = json.loads(request.body)
            logger.debug(f"JSON Params: {params}")
            path = self.get_proxy_path(request)
            params = self.update_payload(request, params)
            middle_resp_ = self.send_request("DELETE", path, json=params)
            response = middle_resp_.json()
        return self.response(response)

    def put(self, request, *args, **kwargs):
        """Put"""
        logger.debug("----- Proxy PUT")
        response = {"status": "error"}
        with logger.catch():
            params = json.loads(request.body)
            logger.debug(f"JSON Params: {params}")
            path = self.get_proxy_path(request)
            params = self.update_payload(request, params)
            middle_resp_ = self.send_request("PUT", path, json=params)
            response = middle_resp_.json()
        return self.response(response)
