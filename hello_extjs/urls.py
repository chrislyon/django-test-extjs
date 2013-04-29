from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('hello_extjs.views',
    (r'^$', 'index'),
    (r'^p1$', 'page1'),
    (r'^p5$', 'page5'),
    (r'^p41$', 'page41'),
    (r'^p42$', 'page42'),
    (r'^p43$', 'page43'),
)
