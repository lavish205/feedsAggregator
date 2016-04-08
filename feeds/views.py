from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import csv_parser, json_parser, xml_parser
from .tasks import save_feeds

class FeedsView(APIView):
    """
    API endpoint that add and list feeds
    """
    def get(self, request, format=None):
        """
        List all feeds based on ranking order by price
        :param request: request object
        :param format: define the output format
        :return:
        """
        pass

    def post(self, request, format=None):
        """
        Parse .xml .json and .csv feed and store it in our data store
        :param request: request object
        :param format: define the output format
        :return:
        """
        save_feeds.delay(self.request.FILES['data'])
        return Response()
