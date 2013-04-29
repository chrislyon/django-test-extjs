from django.conf.urls import patterns, include, url

from testl.models import Contact, ContactForm

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('testl.views',
    ## Liste
    (r'^$', 'liste'),                       ## Index de testl
    (r'^liste$', 'liste'),                  ## Necessaire pour les POST
)
