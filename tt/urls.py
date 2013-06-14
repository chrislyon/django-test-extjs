from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('tt.views',
    (r'^$', 'liste'),
    (r'^create$', 'debug'),
    (r'^read$', 'liste'),
    (r'^update$', 'liste'),
    (r'^destroy$', 'debug'),
)
