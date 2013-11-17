from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('bry1.views',
    ## Debut
    (r'^$', 'index'),
    (r'^(?P<action>p2)$', 'page'),
    (r'^(?P<action>p3)$', 'page'),
)
