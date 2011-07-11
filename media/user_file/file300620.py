import os
import sys

path = '/home/caleb/Documents/Caktus/temp/lib/python2.7/site-packages/django'
if path not in sys.path:
    sys.path.append(path)

sys.path.append("/home/caleb/Documents/Caktus/tutorial/paste")

print (sys.path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()