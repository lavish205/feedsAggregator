from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import FeedsView


urlpatterns = [
    url(r'^feeds/$', FeedsView.as_view()),

    ]