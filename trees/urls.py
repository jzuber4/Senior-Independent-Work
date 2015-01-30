from django.conf.urls import patterns, url

from trees import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^question/$', views.question),
    url(r'^question/(\d+)/$', views.question),
)


