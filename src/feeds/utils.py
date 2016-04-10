from __future__ import absolute_import
import csv
import datetime
import json
from celery import task
from xml.etree import ElementTree as ET
from .models import Product, Ecommerce, Offerings


@task
def extract_data(feeds):
    """
    extract required data from feeds.
    generic method for xml and csv parser as both contains list of dict
    :param feeds:
    :return:
    """
    print "extracting data"
    for feed in feeds:
        # filtering out data for Product table and saving it
        product_query_data = {
            'name': feed.get('product_name'),
            'product_id': feed.get('product_id')
        }
        product = save_products(product_query_data)

        # filtering out data for Ecommerce table and saving it
        ecomm_query_data = {
            'ecomm_id': feed.get('ecomm_id'),
            'name': feed.get('ecomm_portal'),
        }
        ecomm = save_ecommerce(ecomm_query_data)

        # filtering data for Offerings table and saving it
        offering_query_data = {
            'ecommerce': ecomm,
            'product': product,
            'url': feed.get('ecomm_url'),
            'price': feed.get('price'),
            'last_modified': feed.get('last_updated')
        }
        save_offerings(offering_query_data)

@task
def json_parser(data):
    """
    parse json data
    :param data: file data
    :return:
    """
    print "in json parser"
    # deserializing into python
    feeds = json.loads(data.file.getvalue())
    return extract_data(feeds)

@task
def xml_parser(data):
    """
    xml file parser
    :param data:
    :return:
    """
    print "in xml parser"
    xml_data = data.file.getvalue()
    xml_tree = ET.fromstring(xml_data)
    products = list()
    ecommerces = list()
    for elements in xml_tree:
        # filtering out Product data
        product_query_data = {
            'name': elements.find('product_name').text,
            'product_id': elements.find('product_id').text
        }
        product = save_products(product_query_data)

        # filtering out Ecommerce data
        ecomm_query_data = {
            'ecomm_id': elements.find('ecomm_id').text,
            'name': elements.find('ecomm_portal').text
        }
        ecomm = save_ecommerce(ecomm_query_data)

        # filering out Offering data
        offering_query_data = {
            'product': product,
            'ecommerce': ecomm,
            'url': elements.find('ecomm_url').text,
            'price': elements.find('price').text,
            'last_modified': elements.find('last_updated').text

        }
        save_offerings(offering_query_data)
    print products
    return products, ecommerces


def csv_parser(data):
    """
    csv file parser
    :param data:
    :return:
    """
    feeds = csv.DictReader(data.file)
    return extract_data(feeds)


def save_products(product_data):
    """
    create if Product doesn't exists else return the product instance
    :param product_data: product data required for creating new product
    :return: product instance
    """
    product, created = Product.objects.get_or_create(**product_data)
    return product


def save_ecommerce(ecomm_data):
    """
    create if Ecommerce doesn't exists else return the ecommerce instance
    :param ecomm_data: ecommerce data required for creating new ecommerce
    :return: ecommerce instance
    """
    ecomm, created = Ecommerce.objects.get_or_create(**ecomm_data)
    return ecomm


def save_offerings(offering_data):
    """
    create offering if doesn't exists else return the offering instance
    :param offering_data: data required for creating new offering
    :return: offering instance
    """
    product = offering_data.get('product')
    ecommerce = offering_data.get('ecommerce')
    print "in saving offering data"
    try:
        offering = Offerings.objects.get(product=product, ecommerce=ecommerce)

        new_date = datetime.datetime.strptime(
            offering_data['last_modified'], "%Y-%m-%dT%H:%M:%S")

        # removing the timezone awareness
        old_date = offering.last_modified.replace(tzinfo=None)
        # comparing if new data is not outdated
        if old_date <= new_date:
            offering.last_modified = new_date
            offering.price = offering_data.get('price')
            offering.save()

    except Offerings.DoesNotExist:
        Offerings.objects.create(**offering_data)
