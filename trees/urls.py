from django.conf.urls import patterns, url

from trees import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)


