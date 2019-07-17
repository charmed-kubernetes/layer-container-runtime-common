import pytest
from lib.charms.layer.container_runtime_common import (
    merge_config
)


def test_get_hosts():
    CONFIG = {
        'NO_PROXY': '192.168.2.1, 192.168.2.0/29, hello.com',
        'https_proxy': 'https://hop.proxy',
        'HTTP_PROXY': '',

    }
    ENVIRONMENT = {
        'HTTPS_PROXY': 'https://proxy.hop',
        'HTTP_PROXY': 'http://proxy.hop',
        'NO_PROXY': '',
        'no_proxy': 'not tha proxy'
    }

    merged = merge_config(CONFIG, ENVIRONMENT)

    assert merged == {
        'NO_PROXY': '192.168.2.1, 192.168.2.0/29, hello.com',
        'https_proxy': 'https://hop.proxy',
        'http_proxy': 'http://proxy.hop',
        'HTTP_PROXY': 'http://proxy.hop'
    }
