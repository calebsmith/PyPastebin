from django.conf.urls.defaults import *
from pastey import views

urlpatterns = patterns('', 
    (r'^$', views.index), 
    (r'^edit/(?P<edit_id>\d+)/$', views.index),
    (r'^list/$', views.list_page),
    (r'^list/(?P<code_id>\d+)/$', views.list_page),
    (r'^(?P<code_id>\d+)/$', views.detail),
    (r'^detail/(?P<code_id>\d+)/$', views.detail),
    (r'^plain/(?P<code_id>\d+)/$', views.plain),
    (r'^html/(?P<code_id>\d+)/(?P<style_id>\w+)/$', views.html),
) 

