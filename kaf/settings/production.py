from __future__ import absolute_import, unicode_literals

import os
from .base import *
import dj_database_url

DEBUG = False

try:
    from .local import *
except ImportError:
    pass


DATABASES['default'] =  dj_database_url.config()
	
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

#env = os.environ.copy()
SECRET_KEY = "a#yv!z8j(lmrffxxl^+9t!mr)izbrf)7n2cx9(+c$tp1!)j*e5"