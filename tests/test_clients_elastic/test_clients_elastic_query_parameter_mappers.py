import json

import pytest

from app.clients.elastic import query_parameter_mappers
from exceptions.queryexceptions import InvalidInputParameterValue


@pytest.mark.parametrize('param',json.load(open("tests/test_clients_elastic/data/param_examples.json")).items())
def test_parameter_mappers(param):
    """Test each parameter mapper with good and bad inputs"""
    mappers = query_parameter_mappers
    param_name, param_vals = param
    validator = getattr(mappers, param_name)

    validated_param = validator.validate(param_vals['good_raw'])
    assert validated_param == param_vals['validated']

    if param_vals['bad_format_raw'] is not None:
        with pytest.raises(InvalidInputParameterValue):
            validator.validate(param_vals['bad_format_raw'])

    if param_vals['not_allowed_raw'] is not None:
        with pytest.raises(InvalidInputParameterValue):
            validator.validate(param_vals['not_allowed_raw'])
