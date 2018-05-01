"""Pytest Suite to Test app.utils.conversions"""
import pytest

from app.utils.conversions import map_multidict_to_dict, map_content_to_api_spec
from werkzeug.datastructures import MultiDict

def test_map_multidict_to_dict():
    multi = MultiDict([('var1', 'val1'), ('var2', 'val2'), ('var1', 'val2')])
    converted = {'var1': ['val1', 'val2'], 'var2': 'val2'}
    assert map_multidict_to_dict(multi) == converted


def test_map_content_to_api_spec():
    assert map_content_to_api_spec('content') == {'results': 'content'}

