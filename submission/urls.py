from django.conf.urls import patterns, url
from submission.views import add 


urlpatterns = patterns('',
       url(r'^add$', add),
       )
