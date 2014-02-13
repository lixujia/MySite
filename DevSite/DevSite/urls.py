from django.conf.urls import patterns, include, url
from django.conf import settings
from DevSite import filelist
from DevSite import spcproduce
from DevSite import spclist

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DevSite.views.home', name='home'),
    # url(r'^DevSite/', include('DevSite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^files/(.*)$',filelist.static_file_page),
    url(r'^spcproduce/$',spcproduce.spc_produce),
    url(r'^hwtproduce/$',spcproduce.hwt_produce),
    url(r'^hwt-iedinfo/$',spcproduce.hwt_ied_info_xml),
    url(r'^spc/list/(main|extend)$',spclist.show_csv),
)
