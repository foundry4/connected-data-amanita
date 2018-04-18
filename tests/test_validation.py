"""Pytest Suite to test validation tools. Full coverage over processing.py through testing of process_list_content_query_params."""
import pytest

from app.processing import input_query
from app.apiparams.validator import process_list_content_query_params
from exceptions.queryexceptions import InvalidInputQuery
from tests.testdata.querydata import get_multi_query_parameter_test_mappings_restricted, \
    get_multi_query_parameter_test_mappings, multi_input_query_params_multidict_allowed, \
    multi_input_query_params_multidict_some_allowed, multi_input_query_params_multidict_not_allowed, \
    get_single_query_parameter_test_mappings, get_single_query_parameter_test_mappings_restricted, \
    input_query_params_multidict_allowed, input_query_params_multidict_not_allowed, \
    invalid_input_query_params_multidict, \
    empty_input_query_params_multidict, empty_input_query_params_dict

"""Test `process_list_content_query_params()` with test coverage over query parameters passed through with singular & multiple 
values, and over validation against a list of expected parameters and a list of allowed parameter values. """


@pytest.mark.parametrize(
    'mapping', [
        get_multi_query_parameter_test_mappings_restricted(),
        get_multi_query_parameter_test_mappings()
    ]
)
def test_process_query_params_multi_allowed(monkeypatch, mapping):
    """Test when each input query parameter contains multiple values that are allowed.
    case1[success]: only specific values allowed, only specific values passed in
    case2[success]: any values allowed, values passed in"""

    monkeypatch.setattr(input_query, '_get_validators', lambda _: mapping)
    validated_params = process_list_content_query_params(multi_input_query_params_multidict_allowed)
    for param_name, param_list in validated_params.items():
        assert isinstance(param_list, list)
        for param_val in param_list:
            assert isinstance(param_val, mapping[param_name].param_type)


@pytest.mark.parametrize(
    'param_multidict', [
        multi_input_query_params_multidict_some_allowed,
        multi_input_query_params_multidict_not_allowed
    ]
)
def test_process_query_params_multi_not_allowed(monkeypatch, param_multidict):
    """Test when each input query parameter contains multiple values and some/all of the values are not allowed
    case1[fail]: only specific values allowed, only some of the values passed in are allowed
    case2[fail]: only specific values allowed, none of the values passed in are allowed"""
    monkeypatch.setattr(input_query, '_get_validators', lambda _: get_multi_query_parameter_test_mappings_restricted())

    with pytest.raises(InvalidInputQuery):
        process_list_content_query_params(param_multidict)


@pytest.mark.parametrize(
    'mapping', [
        get_single_query_parameter_test_mappings_restricted(),
        get_single_query_parameter_test_mappings()
    ]
)
def test_process_query_params_single_allowed(monkeypatch, mapping):
    """Test when each parameter holds a single value that is allowed
    case1[success]: only specific values allowed, allowed value passed in
    case2[success]: any values allowed, value passed in"""
    monkeypatch.setattr(input_query, '_get_validators', lambda _: mapping)
    validated_params = process_list_content_query_params(input_query_params_multidict_allowed)
    for param_name, param_val in validated_params.items():
        assert isinstance(param_val, mapping[param_name].param_type)


def test_process_query_params_single_not_allowed(monkeypatch):
    """Test when each parameter holds a single value that is not allowed"""
    monkeypatch.setattr(input_query, '_get_validators', lambda _: get_multi_query_parameter_test_mappings_restricted())
    with pytest.raises(InvalidInputQuery):
        process_list_content_query_params(input_query_params_multidict_not_allowed)


def test_process_query_params_invalid_parameter(monkeypatch):
    """Test fail when parameters passed that aren't in the accepted list of params"""
    monkeypatch.setattr(input_query, '_get_validators', lambda _: get_single_query_parameter_test_mappings())
    with pytest.raises(InvalidInputQuery):
        process_list_content_query_params(invalid_input_query_params_multidict)


def test_process_query_params_multi_when_expect_single(monkeypatch):
    """Test fail when api expects a single value and multiple values are given"""
    monkeypatch.setattr(input_query, '_get_validators', lambda _: get_single_query_parameter_test_mappings())
    with pytest.raises(InvalidInputQuery):
        process_list_content_query_params(multi_input_query_params_multidict_allowed)


def test_process_query_params_single_when_expect_multi(monkeypatch):
    """Test query parameter value is cast to list when api expects a list and a single value is given"""
    mapping = get_multi_query_parameter_test_mappings()
    monkeypatch.setattr(input_query, '_get_validators', lambda _: mapping)
    validated_params = process_list_content_query_params(input_query_params_multidict_allowed)
    for param_name, param_val in validated_params.items():
        assert isinstance(param_val, list)
        assert len(param_val) == 1
        assert isinstance(param_val[0], mapping[param_name].param_type)


def test_process_query_params_empty(monkeypatch):
    """Test no failures on no parameters given"""
    monkeypatch.setattr(input_query, '_get_validators', lambda _: get_single_query_parameter_test_mappings())
    validated_params = process_list_content_query_params(empty_input_query_params_multidict)
    assert validated_params == empty_input_query_params_dict
