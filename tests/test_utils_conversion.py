# """Pytest Suite to Test app.utils.conversions"""
# import pytest
#
# from app.utils.conversions import lower_camel_case_to_upper, map_multidict_to_dict, map_content_to_api_spec
# from tests.testdata.querydata import input_query_params_multidict_allowed, input_query_params_dict_allowed, \
#     multi_input_query_params_multidict_allowed, multi_input_query_params_dict_allowed, \
#     empty_input_query_params_multidict, \
#     empty_input_query_params_dict
#
#
# def test_lower_camel_case_to_upper():
#     lower = 'testCase'
#     assert lower_camel_case_to_upper(lower) == 'TestCase'
#     lower_number = '1numberCase'
#     assert lower_camel_case_to_upper(lower_number) == '1numberCase'
#
#
# @pytest.mark.parametrize(
#     'dicts',
#     [
#         (input_query_params_multidict_allowed, input_query_params_dict_allowed),
#         (multi_input_query_params_multidict_allowed, multi_input_query_params_dict_allowed),
#         (empty_input_query_params_multidict, empty_input_query_params_dict)
#     ]
# )
# def test_map_multidict_to_dict(dicts):
#     assert map_multidict_to_dict(dicts[0]) == dicts[1]
#
#
# def test_map_content_to_api_spec():
#     assert map_content_to_api_spec('content') == {'Results': 'content'}
