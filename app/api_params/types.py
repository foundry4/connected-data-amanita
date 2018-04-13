"""Classes to verify and convert special parameter values."""
import dateutil as dateutil
from rdflib import Literal, URIRef

from app.utils.namespaces import namespaces as NS


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


class BoolFromString:
    def __init__(self, bool_str):
        self.bool = True if bool_str in ['true', 'True'] else False

    def __bool__(self):
        return self.bool


class ValidatedDatetime:
    def __init__(self, datetime_str):
        self.datetime = dateutil.parser.parse(datetime_str)

    def __str__(self):
        return str(self.datetime)
