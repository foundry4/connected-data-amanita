import pytest
from rdflib import URIRef

from app.apiparams import lists, types, validator
from app.apiparams.types import BoolFromString, MediaLiteral, LowercaseLiteral, ValidatedDatetime


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
