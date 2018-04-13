import app.api_params.lists as api_validator_lists
import app.api_params.rdf_definitions as api_validators
from app.utils.conversions import map_multidict_to_dict
from exceptions.queryexceptions import InvalidInputParameter, InvalidInputParameterValue, InvalidInputQuery


def process_list_content_query_params(query_params):
    """Process input multidict of params from inbound query to regular dict of params that has
    been validated against a list of expected params and values.

    Arguments:
        query_params (MultiDict): query parameters from HTTP request

    Returns:
        validated_typed_params (dict): parameters that have been validated and cast to the correct type
    """
    query_params_dict = map_multidict_to_dict(query_params)
    validated_typed_params = _validate_param_dict(query_params_dict,
                                                  validator_set='list_content_query_parameter_validators')
    return validated_typed_params


def process_item_query_uri(uri):
    """Convert URI into format compatible with rdflib."""
    validated_typed_uri = api_validators.item_uri_parameter_validator.validate(uri)
    return validated_typed_uri


def process_list_similar_query_params(query_params):
    """Process input multidict of params from inbound query to regular dict of params that has
    been validated against a list of expected params and values.

    Arguments:
        query_params (MultiDict): query parameters from HTTP request

    Returns:
        validated_typed_params (dict): parameters that have been validated and cast to the correct type
    """
    query_params_dict = map_multidict_to_dict(query_params)
    validated_typed_params = _validate_param_dict(query_params_dict,
                                                  validator_set='list_similar_query_parameter_validators')
    return validated_typed_params


def _validate_param_dict(param_dict, validator_set):
    """Iterate through parameters, validate them and cast them to an RDFLib object."""
    validated_typed_params, exceptions = {}, []
    for param, val in param_dict.items():
        try:
            snake_case_name, validated_param = _validate_param(param, val, validator_set)
            validated_typed_params[snake_case_name] = validated_param
        except (InvalidInputParameter, InvalidInputParameterValue) as e:
            exceptions.append(f'{type(e).__name__}: {str(e)}')

    if exceptions:
        raise InvalidInputQuery("Invalid parameters/value(s):\n    %s" % '\n    '.join(exceptions))

    return validated_typed_params


def _validate_param(param_name, param_val, validator_set):
    """Validate and cast a parameter to an RDFLib object."""
    validators = _get_validators(validator_set)
    try:
        validator = validators[param_name]
    except KeyError:
        raise InvalidInputParameter(
            f'Parameter `{param_name}` is not included in the defined parameters {list(validators)}')

    snake_case_name = validator.snake_case_name
    typed_param_val = validator.validate(param_val)

    return snake_case_name, typed_param_val


def _get_validators(validator_set):
    return getattr(api_validator_lists, validator_set)
