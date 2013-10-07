from django.conf.urls import patterns, url
from submission.views import add, submission


urlpatterns = patterns('',
       url(r'^add$', add, name='add_submission'),
       url(r'^submission/(\w+)$', submission, name='submission'),
       )
