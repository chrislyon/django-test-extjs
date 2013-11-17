from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djextjs.views.home', name='home'),
    # url(r'^djextjs/', include('djextjs.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    ##
    url(r'^hello_extjs/', include('hello_extjs.urls')),
    url(r'^contact/', include('contact.urls')),
    url(r'^listed/', include('listed.urls')),
    url(r'^formd/', include('formd.urls')),
    url(r'^notes/', include('notes.urls')),
    url(r'^n2/', include('n2.urls')),
    url(r'^tt/', include('tt.urls')),
    url(r'^bry1/', include('bry1.urls')),
    url(r'^base/', include('base.urls')),
    url(r'^t2/', include('t2.urls')),
)
