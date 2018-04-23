import pytest
from iso8601 import iso8601

from app.apiparams import types
from app.apiparams.types import BoolFromString, MediaUriRef, LowercaseLiteral, ValidatedDatetime, StrictlyPositiveInt, \
    URIStr, LowercaseStr


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

