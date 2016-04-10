from __future__ import absolute_import
from django.conf.urls import url
from .views import FeedsView, FeedsDetailView


urlpatterns = [
    url(r'^feeds/$', FeedsView.as_view()),
    url(r'^feeds/(\d*)/$', FeedsDetailView.as_view()),

    ]
