from __future__ import absolute_import
from celery import task
from django.shortcuts import render
from .utils import csv_parser, json_parser, xml_parser


@task
def save_feeds(data):
    """
    get file data and select the parser to parse that file
    :param data: file data
    :return:
    """
    response = list()
    content_type = {
            'application/json': json_parser,
            'text/xml': xml_parser,
            'text/csv': csv_parser,
        }
    try:
        parser = content_type[data.content_type]
    except Exception:
        pass
    parser.delay(data)
    return response
