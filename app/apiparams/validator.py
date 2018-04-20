from exceptions.queryexceptions import InvalidInputParameterValue


class ParamValidator:
    def __init__(self, snake_case_name, param_type, allowed_values=None, is_list=False, **kwargs):
        """
        Class for storing and validating input query parameters defined in the api spec

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
        """Cast value to type defined in types.py"""
        try:
            if self.is_list:
                v_l = [v] if not isinstance(v, list) else v
                v_cast = [self.param_type(i, **self.kwargs) for i in v_l]
            else:
                v_cast = self.param_type(v, **self.kwargs)
        except Exception as e:
            raise InvalidInputParameterValue(f'Value(s) {v} incorrectly formatted: {str(e)}.')
        return v_cast
