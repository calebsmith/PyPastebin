import os, sys
import site

#project root is 3 parent directories from this file
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
#find the version of python
PYTHON_VERSION = "python" + str(sys.version_info.major) + "." + str(sys.version_info.minor)
#determine the site packages in the environment
SITE_PACKAGES = os.path.join(PROJECT_ROOT, 'env/lib/', PYTHON_VERSION ,'/site-packages')

#add project root to 
sys.path.insert(0, PROJECT_ROOT)
site.addsitedir(os.path.abspath(site_packages))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ['CELERY_LOADER'] = "django"

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()




