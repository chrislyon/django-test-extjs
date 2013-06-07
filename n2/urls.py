from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('n2.views',
    (r'^$', 'liste'),
    (r'^liste$', 'liste'),                  
    (r'^cr/$', 'create'),                  
    (r'^del/(\d+)/$', 'delete'),
    (r'^mod/(\d+)/$', 'modif'),
    (r'^populate$', 'populate'),
)
