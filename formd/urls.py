from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('formd.views',
    (r'^$', 'page1'),                       ## Index de contact
    (r'^p1$', 'page1'),             
)
