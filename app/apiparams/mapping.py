from app.apiparams.lists import get_param_mappers_for_endpoint
from app.utils.conversions import map_multidict_to_dict
from exceptions.queryexceptions import InvalidInputParameterValue, InvalidInputParameter, InvalidInputQuery


class ParameterMapper:
    def __init__(self, snake_case_name, param_type, allowed_values=None, is_list=False, **kwargs):
        """
        Class to cast parameters into a desired type that is compatible with the database to be queried.
        Exceptions are caught for cases in which:
            - A parameter value is passed that is not contained in the `allowed_values` member
            - An incorrect number of parameters is given
            - An exception is raised when casting the value to the desired type

        Arguments:
            snake_case_name (string): the name of the parameter
            param_type (type): the expected type of the parameter, eg Literal or URIRef
            allowed_values (list): allowed values, 'None' for no restrictions
            is_list (bool): if multiple values are expected for this parameter, eg tags
            kwargs (dict): keyword args passed to type on casting eg Literal('example', datatype=XSD.string)
        """
        self.snake_case_name = snake_case_name
        assert type(param_type) == type
        self.param_type = param_type
        self.allowed_values = allowed_values
        self.is_list = is_list
        self.kwargs = kwargs

    def validate(self, v):
        """Check if parameter is has correct number of values, check if these values are expected"""
        self._check_number_vals(v)
        self._check_values_allowed(v)
        v_cast = self._cast_vals(v)
        return v_cast

    def _check_values_allowed(self, v):
        """Check value of parameter against optional list of allowed values specified in types.py"""
        if self.allowed_values is not None:
            v_list = [v] if not isinstance(v, list) else v
            invalid_values = [i for i in v_list if i not in self.allowed_values]
            if invalid_values:
                raise InvalidInputParameterValue(
                    f'Value(s) {invalid_values} not in list of allowed values: {self.allowed_values}')

    def _check_number_vals(self, v):
        """Check multiple values not passed to parameter that only expects one."""
        if isinstance(v, list) and not self.is_list:
            raise InvalidInputParameterValue(
                f'{len(v)} values given to parameter {self.snake_case_name} when single value expected.')

    def _cast_vals(self, v):
        """Cast value to the given `param_type`, catch any exceptions raised.
        Special type definitions exist in `apiparams.types`."""
        try:
            if self.is_list:
                v_l = [v] if not isinstance(v, list) else v
                v_cast = [self.param_type(i, **self.kwargs) for i in v_l]
            else:
                v_cast = self.param_type(v, **self.kwargs)
        except Exception as e:
            raise InvalidInputParameterValue(f'Value(s) {v} incorrectly formatted: {str(e)}.')
        return v_cast



def map_param_values_to_given_definitions(parameter_definitions, endpoint, query_params):
    """Iterate through parameters, cast them to the correct type. On errors in mapping any parameters,
    raise an exception.

    Arguments:
        parameter_definitions (object):  ParameterMapper objects that relate to the given endpoint
        endpoint (str): endpoint for which the parameters will be used for
        path_params (dict): dict of any path parameters to be mapped
        query_params (MultiDict): raw params from http request

    Returns:
        mapped_params: dictionary of mapped params.
    """
    mapped_params, exceptions = {}, []


    validators = get_param_mappers_for_endpoint(endpoint, parameter_definitions)
    for param_name, param_val in query_params.items():
        try:
            validator = validators[param_name]
            mapped_params[validator.snake_case_name] = validator.validate(param_val)
        except KeyError:
            e = InvalidInputParameter(
                f'InvalidInputParameter: Parameter `{param_name}` is not included in the defined parameters '
                f'{list(validators)} for the endpoint "{endpoint}"'
            )
            exceptions.append(f'{type(e).__name__}: {str(e)}')
        except InvalidInputParameterValue as e:
            exceptions.append(f'{type(e).__name__}: {str(e)}')

    if exceptions:
        raise InvalidInputQuery("Invalid parameters/value(s):\n    %s" % '\n    '.join(exceptions))

    return mapped_params
