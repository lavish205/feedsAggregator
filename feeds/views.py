from __future__ import absolute_import
from collections import defaultdict
from django.db.models import F
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Offerings
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
        :return: list of feeds
        """
        query = self.request.query_params.get('query')
        feeds = Offerings.objects.filter(
            product__name__contains=query).annotate(
            product_name=F('product__name'),
            product_id=F('product__product_id'),
            ecomm_name=F('ecommerce__name'),
            ecomm_id=F('ecommerce__ecomm_id')).values('product_name',
                                                      'product_id',
                                                      'ecomm_name',
                                                      'ecomm_id',
                                                      'price'
                                                      ).order_by('price')
        ecommerce = defaultdict(list)
        product = dict()
        for feed in feeds:
            product[feed['product_id']] = feed['product_name']
            ecommerce[feed['product_id']].append(
                {
                    'ecomm_name': feed['ecomm_name'],
                    'price': feed['price']
                }
            )
        response = defaultdict(dict)
        for k, v in product.iteritems():
            response[k]['product_name'] = v
            response[k]['ecomm'] = ecommerce[k]

        return Response(dict(response))

    def post(self, request, format=None):
        """
        Parse .xml .json and .csv feed and store it in our data store
        :param request: request object
        :param format: define the output format
        :return:
        """
        save_feeds.delay(self.request.FILES['data'])
        return Response()
