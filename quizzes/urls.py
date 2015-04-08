from django.conf.urls import patterns, url

from quizzes import views

urlpatterns = patterns('',
    url(r'^$', views.quizzes),
    url(r'^quiz/(\d+)/$', views.quiz),
    url(r'^quiz/(\d+)/question/(\d+)/attempt/(\d+)$', views.question),
)


