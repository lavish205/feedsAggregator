from __future__ import absolute_import
from django.conf.urls import url
from .views import FeedsView


urlpatterns = [
    url(r'^feeds/$', FeedsView.as_view()),

    ]
