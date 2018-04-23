"""Pytest Suite to Test app.utils.conversions"""
import pytest

from app.utils.conversions import lower_camel_case_to_upper, map_multidict_to_dict, map_content_to_api_spec
from werkzeug.datastructures import MultiDict


def test_lower_camel_case_to_upper():
    lower = 'testCase'
    assert lower_camel_case_to_upper(lower) == 'TestCase'
    lower_number = '1numberCase'
    assert lower_camel_case_to_upper(lower_number) == '1numberCase'


def test_map_multidict_to_dict():
    multi = MultiDict([('var1', 'val1'), ('var2', 'val2'), ('var1', 'val2')])
    converted = {'var1': ['val1', 'val2'], 'var2': 'val2'}
    assert map_multidict_to_dict(multi) == converted


def test_map_content_to_api_spec():
    assert map_content_to_api_spec('content') == {'Results': 'content'}
