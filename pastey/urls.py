from django.conf.urls.defaults import *
from pastey import views

urlpatterns = patterns('', 
    (r'^$', views.index), 
    (r'^list.html$', views.list_page),
    (r'^list/(?P<code_id>\d+)/$', views.list_page),
    (r'^(?P<code_id>\d+)/$', views.detail)
)
