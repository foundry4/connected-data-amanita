# # test parameter val dicts here
# from app.apiparams.validator import ParamValidator
# from app.clients import client_interface
#
#
# param_validators = {
#     'paramOne': ParamValidator(
#         snake_case_name='param_one',
#         param_type=str
#     ),
#     'paramTwo': ParamValidator(
#         snake_case_name='param_two',
#         param_type=str
#     ),
# }
#
# input_query_params = {
#     'paramOne': 'val1',
#     'paramTwo': 'val2'
# }
#
# validated_params = {
#     'param_one': 'val1',
#     'param_two': 'val2'
# }
#
#
# class MockClient(client_interface.DBClient):
#     def __init__(self):
#         super().__init__('', '', '')
#
#     def setup_connection(self):
#         pass
#
#     @property
#     def parameter_definitions(self):
#         return None
#
#     def close_connection(self):
#         pass
#
#     @staticmethod
#     def query(query, **params):
#         pass
#
#     def get_content(self, validated_query_params):
#         pass
#
#     def get_item(self, validated_item_uri):
#         pass
#
#     def get_similar(self, validated_item_uri, validated_query_params):
#         pass
#
#
# def test_validate_param_dict(monkeypatch):
#     # have to create child class bc cant instantiate and test abstract base class directly
#     client = MockClient()
#     monkeypatch.setattr(client_interface, 'get_param_validators_for_endpoint', lambda *_: param_validators)
#     validated_params = client._validate_param_dict(input_query_params, 'test')
#     assert validated_params == validated_params
#
