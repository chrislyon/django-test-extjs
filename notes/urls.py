from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('notes.views',
    (r'^$', 'liste'),
    (r'^liste$', 'liste'),                  
    (r'^cr/$', 'create'),                  
    (r'^del/(\d+)/$', 'delete'),
    (r'^mod/(\d+)/$', 'modif'),
)
