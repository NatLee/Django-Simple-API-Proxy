from django.test import TestCase
from mock import Mock, patch
from django_simple_api_proxy.views import APIProxy

class ProxyViewTests(TestCase):

    def test_get(self):
        request = Mock()
        request.return_value = {}
        view = APIProxy()

        with patch.object(APIProxy, 'get') as patched_proxy_method:
            handler = getattr(view, 'get')
            handler(request, 87, foo='bar')

        patched_proxy_method.assert_called_once_with(request, 87, foo='bar')

