from app.apiparams import query_parameter_validators
from app.utils.conversions import map_multidict_to_dict
from exceptions.queryexceptions import InvalidInputParameter, InvalidInputParameterValue, InvalidInputQuery


def process_query_params(query_params):
    """Process input multidict of params from inbound query to regular dict of params that has
    been validated against a list of expected params and values.

    Arguments:
        query_params (MultiDict): query parameters from HTTP request

    Returns:
        validated_typed_params (dict): parameters that have been validated and cast to the correct type
    """
    query_params_dict = map_multidict_to_dict(query_params)
    validated_typed_params = _cast_params_to_rdflib(query_params_dict)

    return validated_typed_params


def _cast_params_to_rdflib(param_dict):
    """Iterate through parameters, validate them and cast them to an RDFLib object."""
    validated_typed_params, exceptions = {}, []
    for param, val in param_dict.items():
        try:
            snake_case_name, validated_param = _cast_param_to_rdflib(param, val)
            validated_typed_params[snake_case_name] = validated_param
        except (InvalidInputParameter, InvalidInputParameterValue) as e:
            exceptions.append(f'{type(e).__name__}: {str(e)}')

    if exceptions:
        raise InvalidInputQuery("Invalid parameters/value(s):\n    %s" % '\n    '.join(exceptions))

    return validated_typed_params


def _cast_param_to_rdflib(param_name, param_val):
    """Validate and cast a parameter to an RDFLib object."""
    try:
        validator = query_parameter_validators[param_name]
    except KeyError:
        raise InvalidInputParameter(
            f'Parameter `{param_name}` is not included in the defined parameters {list(query_parameter_validators)}')

    snake_case_name = validator.snake_case_name
    typed_param_val = validator.validate(param_val)

    return snake_case_name, typed_param_val
