from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

#for static file url patterns - development only
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
   
    url(r'^$', include('pastey.urls')),
    url(r'^pastey/', include('pastey.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
#use static() for development only
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
