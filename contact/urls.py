from django.conf.urls import patterns, include, url

from contact.models import Contact, ContactForm

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('contact.views',
    ## Liste
    (r'^$', 'liste'),                       ## Index de contact
    (r'^liste$', 'liste'),                  ## Necessaire pour les POST
    ## Creation
    url(r'^cr/$', 'create', { 'form':ContactForm, 'template':'contact/create.html', }, name='cr'),
)
