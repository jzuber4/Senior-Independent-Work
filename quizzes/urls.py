from django.conf.urls import patterns, url

from quizzes import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^course/(\d+)/$', views.course),
    url(r'^course/(\d+)/quiz/(\d+)/$', views.quiz),
    url(r'^course/(\d+)/quiz/(\d+)/question/(\d+)/$', views.question),
    url(r'^course/(\d+)/quiz/(\d+)/question/(\d+)/attempt/(\d+)/$', views.attempt),
)


