from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # urls for the quiz site
    url(r'', include('quizzes.urls')),
    # urls for teacher interface
    url(r'^teacher/', include('teacher.urls')),
    # CAS
    url(r'^accounts/login/$', 'cas.views.login', name='login'),
    url(r'^accounts/logout/$', 'cas.views.logout', name='logout'),
    # Admin URLS
    url(r'^admin/', include(admin.site.urls)),
)
