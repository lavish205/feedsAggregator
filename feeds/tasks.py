from celery import task
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
    parser = content_type[data.content_type]
    parser(data)
    return response