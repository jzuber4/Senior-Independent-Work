from django.conf.urls import patterns, url

from teacher import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^course/(\d+)/$', views.course),
    url(r'^course/(\d+)/quiz/create/$', views.create),
    url(r'^course/(\d+)/quiz/(\d+)/edit$', views.edit),
    url(r'^course/(\d+)/quiz/(\d+)/delete$', views.delete),
)


