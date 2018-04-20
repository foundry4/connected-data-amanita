import pytest
from iso8601 import iso8601

from app.apiparams import lists, types
from app.apiparams.types import BoolFromString, MediaUriRef, LowercaseLiteral, ValidatedDatetime, StrictlyPositiveInt, \
    URIStr, LowercaseStr
from app.apiparams.validator import ParamValidator
from exceptions.queryexceptions import InvalidInputParameterValue, InvalidInputParameter, InvalidInputQuery
from app.clients import client_interface


class Definitions:
    def __getattr__(self, item):
        return None


# test parameter lists
def test_correct_content_parameter_list():
    specced_content_parameters = ['mediaType', 'sort', 'maxDuration', 'region', 'publishedAfter', 'categories', 'limit',
                                  'offset', 'random']

    implemented_content_parameters = lists.get_param_validators_for_endpoint('content', Definitions())
    assert sorted(implemented_content_parameters) == sorted(specced_content_parameters)


def test_correct_similar_parameter_list():
    specced_content_parameters = ['mediaType', 'sort', 'maxDuration', 'region', 'publishedAfter', 'limit',
                                  'offset', 'similarityMethod']

    implemented_content_parameters = lists.get_param_validators_for_endpoint('similar', Definitions())
    assert sorted(implemented_content_parameters) == sorted(specced_content_parameters)


def test_correct_item_parameter_list():
    specced_content_parameters = ['itemUri']

    implemented_content_parameters = lists.get_param_validators_for_endpoint('item', Definitions())
    assert sorted(implemented_content_parameters) == sorted(specced_content_parameters)


def test_get_param_invalid_endpoint():
    with pytest.raises(ValueError):
        lists.get_param_validators_for_endpoint('invalid', Definitions())


# test parameter types
def test_bool_from_string():
    bool = BoolFromString('true')
    assert bool
    bool = BoolFromString('True')
    assert bool
    bool = BoolFromString('false')
    assert not bool
    bool = BoolFromString('False')
    assert not bool
    with pytest.raises(ValueError):
        BoolFromString('notbool')


def test_media_literal():
    video = MediaUriRef('video')
    assert video.n3() == '<http://purl.org/dc/terms/MovingImage>'
    audio = MediaUriRef('audio')
    assert audio.n3() == '<http://purl.org/dc/terms/Sound>'
    with pytest.raises(ValueError):
        MediaUriRef('notmedia')


def test_lowercase_literal():
    lowercase = LowercaseLiteral('MixedCase')
    assert lowercase.n3() == '"mixedcase"'


def test_validated_datetime():
    datetime = ValidatedDatetime('19941128T155300')
    assert str(datetime) == '19941128T155300'
    datetime_obj = iso8601.parse_date(datetime)
    assert datetime_obj.year == 1994
    assert datetime_obj.month == 11
    assert datetime_obj.day == 28
    assert datetime_obj.hour == 15
    assert datetime_obj.minute == 53
    assert datetime_obj.second == 0


def test_strictly_positive_int():
    spi = StrictlyPositiveInt(1)
    assert int(spi) == 1
    with pytest.raises(ValueError):
        StrictlyPositiveInt(0)
    with pytest.raises(ValueError):
        StrictlyPositiveInt(-1)


def test_uri_str():
    uri_str = URIStr('http://validuri.com')
    assert uri_str == 'http://validuri.com'
    with pytest.raises(TypeError):
        URIStr(10)
    with pytest.raises(ValueError):
        URIStr(':"}{L"ODF"LSDF')


def test_lowercase_str():
    lowercase = LowercaseStr('MixedCase')
    assert lowercase == 'mixedcase'


def test_parameter_types():
    # fail if new parameter types added or parameter types removed
    defined_parameter_types = [v for v in vars(types) if not v.startswith('_')]
    assert defined_parameter_types == ['iso8601', 'URIRef', 'Literal', 'NS', 'BoolFromString', 'MediaUriRef',
                                       'LowercaseLiteral', 'ValidatedDatetime', 'StrictlyPositiveInt', 'URIStr',
                                       'LowercaseStr']


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
    validator = ParamValidator('test_param', TestTypeFormatted)
    validated_param = validator.validate('correct')
    assert isinstance(validated_param, TestTypeFormatted)
    assert validated_param.val == 'correct'


def test_param_validator_single_val_incorrect_format():
    validator = ParamValidator('test_param', TestTypeFormatted)
    with pytest.raises(InvalidInputParameterValue):
        validator.validate('incorrect')


def test_param_validator_single_val_allowed():
    validator = ParamValidator('test_param', TestType, allowed_values=['allowed'])
    validated_param = validator.validate('allowed')
    assert isinstance(validated_param, TestType)
    assert validated_param.val == 'allowed'


def test_param_validator_single_val_not_allowed():
    validator = ParamValidator('test_param', TestType, allowed_values=['allowed'])
    with pytest.raises(InvalidInputParameterValue):
        validator.validate('notallowed')


def test_param_validator_list_single_correct_format():
    # test list of correctly formatted values (single value)
    validator = ParamValidator('test_param', TestTypeFormatted, is_list=True)
    validated_param = validator.validate('correct')
    assert isinstance(validated_param, list)


def test_param_validator_list_single_incorrect_format():
    # test list of incorrectly formatted values (single value)
    validator = ParamValidator('test_param', TestTypeFormatted, is_list=True)
    with pytest.raises(InvalidInputParameterValue):
        validator.validate('incorrect')


def test_param_validator_list_multiple_correct_format():
    # test list of correctly formatted values (multiple values)
    validator = ParamValidator('test_param', TestTypeFormatted, is_list=True)
    validated_param = validator.validate(['correct', 'correct'])
    assert isinstance(validated_param, list)
    assert all(isinstance(param, TestTypeFormatted) for param in validated_param)
    assert all(param.val == 'correct' for param in validated_param)


def test_param_validator_list_multiple_incorrect_format():
    # test list of incorrectly formatted values (multiple values)
    validator = ParamValidator('test_param', TestTypeFormatted, is_list=True)
    with pytest.raises(InvalidInputParameterValue):
        validator.validate(['incorrect', 'incorrect'])


def test_param_validator_list_multiple_mixed_format():
    # test list of mixed formatted values (multiple values)
    validator = ParamValidator('test_param', TestTypeFormatted, is_list=True)
    with pytest.raises(InvalidInputParameterValue):
        validator.validate(['correct', 'incorrect'])


def test_param_validator_list_single_allowed():
    validator = ParamValidator('test_param', TestType, allowed_values=['allowed'], is_list=True)
    validated_param = validator.validate('allowed')
    assert isinstance(validated_param, list)


def test_param_validator_list_single_not_allowed():
    # test list of non allowed values (single value)
    validator = ParamValidator('test_param', TestType, allowed_values=['allowed'], is_list=True)
    with pytest.raises(InvalidInputParameterValue):
        validator.validate('notallowed')


def test_param_validator_list_multiple_allowed():
    # test list of allowed values (multiple values)
    validator = ParamValidator('test_param', TestType, allowed_values=['allowed'], is_list=True)
    validated_param = validator.validate(['allowed', 'allowed'])
    assert isinstance(validated_param, list)
    assert all(isinstance(param, TestType) for param in validated_param)
    assert all(param.val == 'allowed' for param in validated_param)


def test_param_validator_list_multiple_not_allowed():
    # test list of not allowed values (multiple values)
    validator = ParamValidator('test_param', TestType, allowed_values=['allowed'], is_list=True)
    with pytest.raises(InvalidInputParameterValue):
        validator.validate(['notallowed', 'notallowed'])


def test_param_validator_list_multiple_mixed_allowed():
    validator = ParamValidator('test_param', TestType, allowed_values=['allowed'], is_list=True)
    # test list of mixed allowed values (multiple values)
    with pytest.raises(InvalidInputParameterValue):
        validator.validate(['allowed', 'notallowed'])


def test_param_validator_list_expecting_single():
    validator = ParamValidator('test_param', TestTypeFormatted, is_list=False)
    with pytest.raises(InvalidInputParameterValue):
        validator.validate(['correct', 'correct'])


# test protected _validate_param_dict method
# have to create child class because cant instantiate and test abstract base class directly

param_validators = {
    'paramOne': ParamValidator(
        snake_case_name='param_one',
        param_type=str
    ),
    'paramTwo': ParamValidator(
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

validated_params = {
    'param_one': 'val1',
    'param_two': 'val2'
}


class MockClient(client_interface.DBClient):
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

    def get_content(self, validated_query_params):
        pass

    def get_item(self, validated_item_uri):
        pass

    def get_similar(self, validated_item_uri, validated_query_params):
        pass


def test_validate_param_dict(monkeypatch):
    client = MockClient()
    monkeypatch.setattr(client_interface, 'get_param_validators_for_endpoint', lambda *_: param_validators)
    validated_params = client._validate_param_dict(existing_input_query_params, 'test')
    assert validated_params == validated_params

    with pytest.raises(InvalidInputQuery):
        client._validate_param_dict(non_existing_input_query_params, 'test')
