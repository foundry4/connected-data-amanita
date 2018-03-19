from rdflib import Literal, URIRef
from rdflib.namespace import XSD
from app.utils.namespaces import namespaces as NS

from app.utils.validation import ParamValidator

response_fields = ['programme', 'medium', 'duration', 'publicationDate', 'masterbrand', 'genre']


class MediaLiteral():
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


query_parameter_validators = {
    'media': ParamValidator(
        snake_case_name='media',
        param_type=MediaLiteral,
        allowed_values=['video', 'audio'],
        is_list=True,
    ),
    'sort': ParamValidator(
        snake_case_name='sort',
        param_type=str,
        is_list=False,
        allowed_values=response_fields + [f'-{field}' for field in response_fields]
    ),
    'maxDuration': ParamValidator(
        snake_case_name='max_duration',
        param_type=Literal,
        is_list=False,
        datatype=XSD.duration
    ),
    'region': ParamValidator(
        snake_case_name='region',
        param_type=Literal,
        is_list=False,
        allowed_values=['uk', 'ex-uk'],
        datatype=XSD.string
    ),
    'publishedAfter': ParamValidator(
        snake_case_name='published_after',
        param_type=Literal,
        is_list=False,
        datatype=XSD.datetime
    ),
    'categories': ParamValidator(
        snake_case_name='categories',
        param_type=Literal,
        is_list=True,
    ),
    'tags': ParamValidator(
        snake_case_name='tags',
        param_type=URIRef,
        is_list=True
    ),
    'limit': ParamValidator(
        snake_case_name='limit',
        param_type=int,
        is_list=False
    ),
    'offset': ParamValidator(
        snake_case_name='offset',
        param_type=int,
        is_list=False
    )
}
