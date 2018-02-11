from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    # /api/threat/ip/x.x.x.x
    # url(r'^threat/$', views.APIRoot.as_view()),
    url(r'^threat/ip/(?P<ip>.+)/?$', views.IPDetailsView.as_view()),
    url(r'^traffic/$', views.TrafficView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)