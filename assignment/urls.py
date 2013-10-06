from django.conf.urls import patterns, url
from assignment.views import assignments, assignment


urlpatterns = patterns('',
       url(r'^$', assignments),
       url(r'^(\d+)$', assignment),
       )
