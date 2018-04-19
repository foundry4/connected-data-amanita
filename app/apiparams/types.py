import iso8601
from rdflib import URIRef, Literal

from app.clients.sparql.namespaces import namespaces as NS


class BoolFromString:
    def __init__(self, bool_str):
        if bool_str not in ['true', 'True', 'false', 'False']:
            raise ValueError(f'"{bool_str}" is not a valid boolean string.')
        real_bool = True if bool_str in ['true', 'True'] else False
        self.bool = real_bool

    def __bool__(self):
        return self.bool


class MediaUriRef(URIRef):
    def __new__(cls, media_str):
        if media_str == 'video':
            uriref = NS['dct'].MovingImage
        elif media_str == 'audio':
            uriref = NS['dct'].Sound
        else:
            raise ValueError('Invalid media type.')
        return URIRef(uriref)


class LowercaseLiteral(Literal):
    def __new__(cls, str_lit):
        return Literal(str_lit.lower())


class ValidatedDatetime(str):
    def __new__(cls, datetime: str):
        datetime = datetime[1:] if datetime.startswith('P') else datetime
        iso8601.parse_date(datetime)
        return datetime


class StrictlyPositiveInt(int):
    def __new__(cls, integer):
        integer = int(integer)
        if integer < 1:
            raise ValueError('Integer must be greater than 0.')
        return int(integer)


class URIStr(str):
    def __new__(cls, uri_str):
        u = URIRef(uri_str)
        try:
            u.n3()
        except Exception:
            raise ValueError(f'{uri_str} does not look like a valid URI.')
        return uri_str


class LowercaseStr(str):
    def __new__(cls, string):
        if not isinstance(string, str):
            raise TypeError(f'"{string}" is not a string.')
        return string.lower()
