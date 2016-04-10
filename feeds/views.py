from __future__ import absolute_import
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Offerings, Product
from .tasks import save_feeds


class FeedsView(APIView):
    """
    API endpoint that allow you to search and list feeds
    """
    def get(self, request, format=None):
        """
        List all feeds
        :param request: request object
        :param format: define the output format
        :return: list of feeds
        """
        query = self.request.query_params.get('query')
        if not query:
            return render(request, 'index.html')

        products = Product.objects.filter(name__contains=query)
        response = list()
        for product in products:
            response.append({
                'name': product.name,
                'id': product.product_id
            })
        print response
        context = {'response': response}
        return render(request, 'index.html', context)

    def post(self, request, format=None):
        """
        Parse .xml .json and .csv feed and store it in our data store
        :param request: request object
        :param format: define the output format
        :return: return 201
        """
        save_feeds.delay(self.request.FILES['data'])
        return Response(status=201)


class FeedsDetailView(APIView):
    """
    API endpoint that provide details of feed
    """
    def get(self, request, pk, format=None):
        """
        provide details of selected feed based on ranking order by price
        :param request: request object
        :param pk: pk of feed
        :param format: format of output
        :return: 200, and details of feed
        """
        try:
            feed = Product.objects.get(pk=pk)
            offerings = feed.offerings.all().order_by('price')
            response = dict()
            response["name"] = feed.name
            response["ecomms"] = list()
            for offering in offerings:
                response["ecomms"].append({
                    "name": offering.ecommerce.name,
                    "price": offering.price,
                    "url": offering.url
                })
            return render(request, 'feedDetails.html', response)
        except Product.DoesNotExist:
            return Response(status=404)
