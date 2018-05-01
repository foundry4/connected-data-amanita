import pytest

from app.apiparams import mapping
from app.apiparams.mapping import ParameterMapper, map_param_values_to_given_definitions
from app.clients import client_superclass
from exceptions.queryexceptions import InvalidInputParameterValue, InvalidInputQuery


class TestTypeFormatted:
    def __init__(self, value):
        if value == 'correct':
            self.val = value
        else:
            raise ValueError('Incorrect input.')


class TestType:
    def __init__(self, value):
        self.val = value


# test validator class
def test_param_validator_single_val_correct_format():
    # test single correctly formatted
    validator = ParameterMapper('test_param', TestTypeFormatted)
    validated_param = validator.validate('correct')
    assert isinstance(validated_param, TestTypeFormatted)
    assert validated_param.val == 'correct'


def test_param_validator_single_val_incorrect_format():
    validator = ParameterMapper('test_param', TestTypeFormatted)
    with pytest.raises(InvalidInputParameterValue):
        validator.validate('incorrect')


def test_param_validator_single_val_allowed():
    validator = ParameterMapper('test_param', TestType, allowed_values=['allowed'])
    validated_param = validator.validate('allowed')
    assert isinstance(validated_param, TestType)
    assert validated_param.val == 'allowed'


def test_param_validator_single_val_not_allowed():
    validator = ParameterMapper('test_param', TestType, allowed_values=['allowed'])
    with pytest.raises(InvalidInputParameterValue):
        validator.validate('notallowed')


def test_param_validator_list_single_correct_format():
    # test list of correctly formatted values (single value)
    validator = ParameterMapper('test_param', TestTypeFormatted, is_list=True)
    validated_param = validator.validate('correct')
    assert isinstance(validated_param, list)


def test_param_validator_list_single_incorrect_format():
    # test list of incorrectly formatted values (single value)
    validator = ParameterMapper('test_param', TestTypeFormatted, is_list=True)
    with pytest.raises(InvalidInputParameterValue):
        validator.validate('incorrect')


def test_param_validator_list_multiple_correct_format():
    # test list of correctly formatted values (multiple values)
    validator = ParameterMapper('test_param', TestTypeFormatted, is_list=True)
    validated_param = validator.validate(['correct', 'correct'])
    assert isinstance(validated_param, list)
    assert all(isinstance(param, TestTypeFormatted) for param in validated_param)
    assert all(param.val == 'correct' for param in validated_param)


def test_param_validator_list_multiple_incorrect_format():
    # test list of incorrectly formatted values (multiple values)
    validator = ParameterMapper('test_param', TestTypeFormatted, is_list=True)
    with pytest.raises(InvalidInputParameterValue):
        validator.validate(['incorrect', 'incorrect'])


def test_param_validator_list_multiple_mixed_format():
    # test list of mixed formatted values (multiple values)
    validator = ParameterMapper('test_param', TestTypeFormatted, is_list=True)
    with pytest.raises(InvalidInputParameterValue):
        validator.validate(['correct', 'incorrect'])


def test_param_validator_list_single_allowed():
    validator = ParameterMapper('test_param', TestType, allowed_values=['allowed'], is_list=True)
    validated_param = validator.validate('allowed')
    assert isinstance(validated_param, list)


def test_param_validator_list_single_not_allowed():
    # test list of non allowed values (single value)
    validator = ParameterMapper('test_param', TestType, allowed_values=['allowed'], is_list=True)
    with pytest.raises(InvalidInputParameterValue):
        validator.validate('notallowed')


def test_param_validator_list_multiple_allowed():
    # test list of allowed values (multiple values)
    validator = ParameterMapper('test_param', TestType, allowed_values=['allowed'], is_list=True)
    validated_param = validator.validate(['allowed', 'allowed'])
    assert isinstance(validated_param, list)
    assert all(isinstance(param, TestType) for param in validated_param)
    assert all(param.val == 'allowed' for param in validated_param)


def test_param_validator_list_multiple_not_allowed():
    # test list of not allowed values (multiple values)
    validator = ParameterMapper('test_param', TestType, allowed_values=['allowed'], is_list=True)
    with pytest.raises(InvalidInputParameterValue):
        validator.validate(['notallowed', 'notallowed'])


def test_param_validator_list_multiple_mixed_allowed():
    validator = ParameterMapper('test_param', TestType, allowed_values=['allowed'], is_list=True)
    # test list of mixed allowed values (multiple values)
    with pytest.raises(InvalidInputParameterValue):
        validator.validate(['allowed', 'notallowed'])


def test_param_validator_list_expecting_single():
    validator = ParameterMapper('test_param', TestTypeFormatted, is_list=False)
    with pytest.raises(InvalidInputParameterValue):
        validator.validate(['correct', 'correct'])


# test protected map_param_values_to_given_definitions method
# have to create child class because cant instantiate and test abstract base class directly

param_mappers = {
    'paramOne': ParameterMapper(
        snake_case_name='param_one',
        param_type=str
    ),
    'paramTwo': ParameterMapper(
        snake_case_name='param_two',
        param_type=str
    ),
}

existing_input_query_params = {
    'paramOne': 'val1',
    'paramTwo': 'val2'
}

non_existing_input_query_params = {
    'paramOne': 'val1',
    'paramThree': 'val3'
}

mapped_params = {
    'param_one': 'val1',
    'param_two': 'val2'
}


class MockClient(client_superclass.DBClient):
    def __init__(self):
        super().__init__('', '', '')

    def setup_connection(self):
        pass

    @property
    def parameter_definitions(self):
        return None

    def close_connection(self):
        pass

    @staticmethod
    def query(query, **params):
        pass

    def get_content(self, mapped_params):
        pass

    def get_item(self, mapped_params):
        pass

    def get_similar(self,mapped_paramss):
        pass


def test_map_param_values_to_db_compatible(monkeypatch):
    monkeypatch.setattr(mapping, 'get_param_mappers_for_endpoint', lambda *_: param_mappers)
    validated_params = map_param_values_to_given_definitions(existing_input_query_params, 'test', None)
    assert validated_params == validated_params

    with pytest.raises(InvalidInputQuery):
        map_param_values_to_given_definitions(None, 'test', non_existing_input_query_params)
