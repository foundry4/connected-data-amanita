"""Definitions of API parameter validators for all endpoints for Elasticsearch only."""

from app.apiparams.types import BoolFromString, ValidatedDatetime, StrictlyPositiveInt, LowercaseLiteral, URIStr, \
    LowercaseStr
from app.apiparams.mapping import ParameterMapper

sortable_fields = ['duration', 'publicationDate', 'masterBrand']

item_uri = ParameterMapper(
    snake_case_name='item_uri',
    param_type=URIStr,
    is_list=False
)
media_type = ParameterMapper(
    snake_case_name='media_type',
    param_type=str,
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
    param_type=StrictlyPositiveInt,
    is_list=False,
)
region = ParameterMapper(
    snake_case_name='region',
    param_type=str,
    is_list=False,
    allowed_values=['uk', 'ex-uk'],
)
published_after = ParameterMapper(
    snake_case_name='published_after',
    param_type=ValidatedDatetime,
    is_list=False,
)
categories = ParameterMapper(
    snake_case_name='categories',
    param_type=LowercaseStr,
    is_list=True,
)
limit = ParameterMapper(
    snake_case_name='limit',
    param_type=StrictlyPositiveInt,
    is_list=False
)
offset = ParameterMapper(
    snake_case_name='offset',
    param_type=StrictlyPositiveInt,
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
    allowed_values=['genre', 'masterBrand']
)
