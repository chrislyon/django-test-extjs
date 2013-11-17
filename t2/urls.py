from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('t2.views',
    (r'^$', 'index'),
    (r'^(?P<action>update)$', 'debug'),
)
