from rdflib import Literal, URIRef
from rdflib.namespace import XSD

from app.utils.validation import ParamValidator


# TODO: DATALAB-150: stardog content needs to be re-ingested, changes to be reflected here to mirror latest api spec
# TODO implement sort
# todo: fix duration on ingest
# todo: need things like embargoes on filter?
# todo: implement date on translator

#
# class ValidatedSortLiteral():
#     def __init__(self, sort_string, datatype):
#         if sort_string[0] not in ['+', '-']:
#             raise InvalidInputParameterValue('The first character of the sort value must be either "+" (ASC) or "-" '
#                                              f'(DESC), given value is {sort_string[0]}.')
#         if sort_string[1:] not in response_fields:
#             raise InvalidInputParameterValue(f'The given field, "{sort_string[1:]}", cannot be sorted by. Allowed fields are {response_fields}.')

response_fields = ['programme', 'medium', 'duration', 'publicationDate', 'masterbrand', 'genre']


query_parameter_validators = {
    'media': ParamValidator(
        name='media',
        param_type=Literal,
        allowed_values=['Video', 'Audio', 'Text'],
        is_list=True,
        datatype=XSD.string
    ),
    'sort': ParamValidator(
        name='sort',
        param_type=str,
        is_list=False,
        allowed_values=['+'+f for f in response_fields] + ['-'+f for f in response_fields]
    ),
    'maxDuration': ParamValidator(
        name='maxDuration',
        param_type=Literal,
        is_list=False,
        datatype=XSD.duration
    ),
    'region': ParamValidator(
        name='region',
        param_type=Literal,
        is_list=False,
        allowed_values=['uk', 'ex-uk'],
        datatype=XSD.string
    ),
    'publishedAfter': ParamValidator(
        name='publishedAfter',
        param_type=Literal,
        is_list=False,
        datatype=XSD.datetime
    ),
    'categories': ParamValidator(
        name='categories',
        param_type=Literal,
        is_list=True,
        datatype=XSD.string
    ),
    'tags': ParamValidator(
        name='tags',
        param_type=URIRef,
        is_list=True,
    ),
    'limit': ParamValidator(
        name='limit',
        param_type=int,
        is_list=False
    ),
    'offset': ParamValidator(
        name='offset',
        param_type=int,
        is_list=False
    )
}
