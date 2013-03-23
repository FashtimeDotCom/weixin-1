#encoding:utf8

import os
import sys

path='/var/www/weixin'
os.environ['DJANGO_SETTINGS_MODULE'] = 'weixin.settings'
os.environ['PYTHON_EGG_CACHE'] = '/tmp/.python-eggs'

if path not in sys.path:
    sys.path.append(path)

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

