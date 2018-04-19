import json

import pytest

from app.clients.elastic import query_param_definitions
from exceptions.queryexceptions import InvalidInputParameterValue


@pytest.mark.parametrize('param',json.load(open("test_elastic_client/data/param_examples.json")).items())
def test_parameter_definitions(param):
    definitions = query_param_definitions
    param_name, param_vals = param
    validator = getattr(definitions, param_name)

    validated_param = validator.validate(param_vals['good_raw'])
    assert validated_param == param_vals['validated']

    if param_vals['bad_format_raw'] is not None:
        with pytest.raises(InvalidInputParameterValue):
            validator.validate(param_vals['bad_format_raw'])

    if param_vals['not_allowed_raw'] is not None:
        with pytest.raises(InvalidInputParameterValue):
            validator.validate(param_vals['not_allowed_raw'])
