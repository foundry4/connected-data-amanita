"""MockDefinitions of API parameter validators for all endpoints for Elasticsearch only."""

from app.apiparams.types import ValidatedDatetime, StrictlyPositiveInt, URIStr, \
    LowercaseStr, DashSortFromRPC
from app.apiparams.mapping import ParameterMapper

sortable_fields = ['DURATION', 'MEDIA', 'MASTER_BRAND']

item_uri = ParameterMapper(
    snake_case_name='item_uri',
    param_type=URIStr,
    is_list=False
)
media_type = ParameterMapper(
    snake_case_name='media_type',
    param_type=LowercaseStr,
    allowed_values=['VIDEO', 'AUDIO'],
    is_list=True,
)

sort = ParameterMapper(
    snake_case_name='sort',
    param_type=DashSortFromRPC,
    is_list=True,
    allowed_values=[f'{field}_{direction}' for field in sortable_fields for direction in ['ASC', 'DESC']]
)
max_duration = ParameterMapper(
    snake_case_name='max_duration',
    param_type=StrictlyPositiveInt,
    is_list=False,
)
region = ParameterMapper(
    snake_case_name='region',
    param_type=LowercaseStr,
    is_list=False,
    allowed_values=['UK', 'EX-UK', 'WORLDWIDE'],
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
    param_type=bool,
    is_list=False,
)

