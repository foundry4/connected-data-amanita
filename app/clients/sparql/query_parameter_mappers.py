"""MockDefinitions of API parameters for all endpoints."""
from rdflib import URIRef, Literal, XSD

from app.apiparams.types import BoolFromString, MediaUriRef, LowercaseLiteral
from app.apiparams.mapping import ParameterMapper

sortable_fields = ['duration', 'publicationDate', 'masterBrand']

item_uri = ParameterMapper(
    snake_case_name='item_uri',
    param_type=URIRef,
    is_list=False
)

media_type = ParameterMapper(
    snake_case_name='media_type',
    param_type=MediaUriRef,
    allowed_values=['video', 'audio'],
    is_list=True,
)

sort = ParameterMapper(
    snake_case_name='sort',
    param_type=str,
    is_list=True,
    allowed_values=sortable_fields + [f'-{field}' for field in sortable_fields]
)
max_duration = ParameterMapper(
    snake_case_name='max_duration',
    param_type=Literal,
    is_list=False,
    datatype=XSD.duration
)
region = ParameterMapper(
    snake_case_name='region',
    param_type=Literal,
    is_list=False,
    allowed_values=['uk', 'ex-uk'],
    datatype=XSD.string
)
published_after = ParameterMapper(
    snake_case_name='published_after',
    param_type=Literal,
    is_list=False,
    datatype=XSD.datetime
)
categories = ParameterMapper(
    snake_case_name='categories',
    param_type=LowercaseLiteral,
    is_list=True,
)

tags = ParameterMapper(
    snake_case_name='tags',
    param_type=URIRef,
    is_list=True
)
limit = ParameterMapper(
    snake_case_name='limit',
    param_type=int,
    is_list=False
)
offset = ParameterMapper(
    snake_case_name='offset',
    param_type=int,
    is_list=False
)
random = ParameterMapper(
    snake_case_name='random',
    param_type=BoolFromString,
    is_list=False,
    allowed_values=['true', 'false']
)

similarity_method = ParameterMapper(
    snake_case_name='similarity_method',
    param_type=str,
    is_list=False,
    allowed_values=['genre', 'tag', 'masterBrand']
)
