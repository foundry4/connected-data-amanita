import pytest
from rdflib import URIRef

from app.apiparams import lists, types, validator
from app.apiparams.types import BoolFromString, MediaLiteral, LowercaseLiteral, ValidatedDatetime
from app.apiparams.validator import ParamValidator
from exceptions.queryexceptions import InvalidInputParameterValue


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
    specced_content_parameters = ['item_uri']

    implemented_content_parameters = lists.get_param_validators_for_endpoint('item', Definitions())
    assert sorted(implemented_content_parameters) == sorted(specced_content_parameters)


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
    video = MediaLiteral('video')
    assert video.n3() == '<http://purl.org/dc/terms/MovingImage>'
    audio = MediaLiteral('audio')
    assert audio.n3() == '<http://purl.org/dc/terms/Sound>'
    with pytest.raises(ValueError):
        MediaLiteral('notmedia')


def test_lowercase_literal():
    lowercase = LowercaseLiteral('MixedCase')
    assert lowercase.n3() == '"mixedcase"'


def test_validated_datetime():
    datetime = ValidatedDatetime('19941128T155300')
    assert str(datetime) == '19941128T155300'
    datetime_obj = datetime.datetime_obj
    assert datetime_obj.year == 1994
    assert datetime_obj.month == 11
    assert datetime_obj.day == 28
    assert datetime_obj.hour == 15
    assert datetime_obj.minute == 53
    assert datetime_obj.second == 0


def test_parameter_types():
    # fail if new parameter types added or parameter types removed
    defined_parameter_types = [v for v in vars(types) if not v.startswith('_')]
    assert defined_parameter_types == ['iso8601', 'URIRef', 'Literal', 'NS', 'BoolFromString', 'MediaLiteral', 'LowercaseLiteral', 'ValidatedDatetime']

# test validator class
def test_param_validator():
    class TestValue:
        def __init__(self, value):
            if value == 'correct':
                self.val = value
            else:
                raise ValueError('Incorrect input.')

    class TestAllowedValues:
        def __init__(self, value):
            self.val = value

    # test single correctly formatted
    validator = ParamValidator('test_param', TestValue)
    validated_param = validator.validate('correct')
    assert isinstance(validated_param, TestValue)
    assert validated_param.val == 'correct'
    # test incorrectly formatted value
    with pytest.raises(ValueError):
        validator.validate('incorrect')
    # test allowed value
    validator = ParamValidator('test_param', TestAllowedValues, allowed_values=['allowed'])
    validated_param = validator.validate('allowed')
    assert isinstance(validated_param, TestAllowedValues)
    assert validated_param.val == 'allowed'
    # test not allowed value
    with pytest.raises(InvalidInputParameterValue):
        validator.validate('notallowed')
    # test list of correctly formatted values (single value)
    validator = ParamValidator('test_param', TestValue, is_list=True)
    validated_param = validator.validate('correct')
    assert isinstance(validated_param, list)
    # test list of incorrectly formatted values (single value)
    with pytest.raises(ValueError):
        validator.validate('incorrect')
    # test list of correctly formatted values (multiple values)
    validated_param = validator.validate(['correct', 'correct'])
    assert isinstance(validated_param, list)
    assert all(isinstance(param, TestValue) for param in validated_param)
    assert all(param.val == 'correct' for param in validated_param)
    # test list of incorrectly formatted values (multiple values)
    with pytest.raises(ValueError):
        validator.validate(['incorrect','incorrect'])
    # test list of mixed formatted values (multiple values)
    with pytest.raises(ValueError):
        validator.validate(['correct', 'incorrect'])
    # test list of allowed values
    validator = ParamValidator('test_param', TestAllowedValues, allowed_values=['allowed'], is_list=True)
    validated_param = validator.validate('allowed')
    assert isinstance(validated_param, list)
    # test list of non allowed values (single value)
    with pytest.raises(InvalidInputParameterValue):
        validator.validate('notallowed')
    # test list of allowed values (multiple values)
    validated_param = validator.validate(['allowed', 'allowed'])
    assert isinstance(validated_param, list)
    assert all(isinstance(param, TestAllowedValues) for param in validated_param)
    assert all(param.val == 'allowed' for param in validated_param)
    # test list of not allowed values (multiple values)
    with pytest.raises(InvalidInputParameterValue):
        validator.validate(['notallowed', 'notallowed'])
    # test list of mixed allowed values (multiple values)
    with pytest.raises(InvalidInputParameterValue):
        validator.validate(['allowed', 'notallowed'])