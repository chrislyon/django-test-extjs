from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('listed.views',
    ## Liste
    (r'^$', 'liste'),                       ## Index de contact
    (r'^liste$', 'liste'),                  
    (r'^liste_data$', 'liste_data'),             
)
