from django.conf.urls import patterns, include, url
from django.conf import settings
from FileServe import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'FileServe.views.home', name='home'),
    # url(r'^FileServe/', include('FileServe.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

                       (r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
                       (r'^files/(.*)$',views.static_file_page),
)
