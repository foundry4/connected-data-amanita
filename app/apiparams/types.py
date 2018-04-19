import iso8601
from rdflib import URIRef, Literal

from app.clients.sparql.namespaces import namespaces as NS



class BoolFromString:
    def __init__(self, bool_str):
        if bool_str not in ['true', 'True', 'false', 'False']:
            raise ValueError(f'"{bool_str}" is not a valid boolean string.')
        self.bool = True if bool_str in ['true', 'True'] else False

    def __bool__(self):
        return self.bool


class MediaLiteral:
    def __init__(self, media_str):
        if media_str == 'video':
            media_lit = URIRef(NS['dct'].MovingImage)
        elif media_str == 'audio':
            media_lit = URIRef(NS['dct'].Sound)
        else:
            raise ValueError('Invalid media type.')
        self.media_lit = media_lit

    def n3(self):
        return self.media_lit.n3()


class LowercaseLiteral:
    def __init__(self, str_lit):
        self.str_lit = Literal(str_lit.lower())

    def n3(self):
        return self.str_lit.n3()


class ValidatedDatetime:
    def __init__(self, datetime: str):
        datetime = datetime[1:] if datetime.startswith('P') else datetime
        self.datetime_obj = iso8601.parse_date(datetime)
        self.datetime = datetime

    def __str__(self):
        return self.datetime

