from dateutil import parser
from rdflib import URIRef, Literal

from app.clients.sparql.namespaces import namespaces as NS


class BoolFromString:
    def __init__(self, bool_str):
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
    def __init__(self, datetime_str):
        self.datetime = parser.parse(datetime_str)

    def __str__(self):
        return str(self.datetime)
