from django.conf.urls import patterns, url
from assignment.views import assignments, assignment, report


urlpatterns = patterns('',
       url(r'^$', assignments, name='assignments'),
       url(r'^(\d+)$', assignment, name='assignment'),
       url(r'^report/(\d+)$', report, name='report'),
       )
