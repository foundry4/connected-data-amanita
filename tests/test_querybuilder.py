"""Pytest Suite to test querybuilder"""
import pytest
from pyparsing import ParseException
from rdflib import Graph, Literal, XSD

from app.querybuilder.sparql import build_get_content_query
from app.utils.namespaces import namespaces


def test_build_get_content_query_syntax_no_params():
    """Test syntax of generated queries by querying on rdflib Graph instance with no query parameters."""
    g = Graph()
    q = build_get_content_query()
    qres = g.query(q, initNs=namespaces)
    assert qres.bindings == [{}]


real_params = {
    'media': [Literal('Video', datatype=XSD.string), Literal('Audio', datatype=XSD.string)],
    'tags': [Literal('tag1', datatype=XSD.string)],
    'limit': 20,
    'offset': 0,
    'sort': 'duration',
    'region': Literal('uk', datatype=XSD.string),
    'published_after': Literal('2012-02-17T13:00:10', datatype=XSD.datetime),
    'categories': [Literal('genre1', datatype=XSD.string), Literal('genre2', datatype=XSD.string)]
}


@pytest.mark.parametrize('params', list(real_params.items()))
def test_build_get_content_query_syntax_params_individual(params):
    """Test syntax of generated queries by querying on rdflib Graph instance with query parameters."""
    g = Graph()
    q = build_get_content_query(**{params[0]: params[1]})
    qres = g.query(q, initNs=namespaces)
    assert qres.bindings == [{}]


def test_build_get_content_query_syntax_params_all():
    """Test syntax of generated queries by querying on rdflib Graph instance with query parameters."""
    g = Graph()
    q = build_get_content_query(**real_params)
    qres = g.query(q, initNs=namespaces)
    assert qres.bindings == [{}]


def test_build_get_content_query_syntax_fail():
    g = Graph()
    q = 'invalid spaqrl query'
    with pytest.raises(ParseException):
        g.query(q)
