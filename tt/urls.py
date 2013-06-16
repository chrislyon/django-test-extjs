from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

#   url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),

urlpatterns = patterns('tt.views',
    (r'^$', 'liste'),
    (r'^(?P<action>create)$', 'debug'),
    (r'^(?P<action>read)$', 'liste'),
    (r'^(?P<action>update)$', 'update'),
    (r'^(?P<action>destroy)$', 'debug'),
)
