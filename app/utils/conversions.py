"""Functions to map/convert simple data."""
from google.protobuf.pyext._message import RepeatedScalarContainer

def map_multidict_to_dict(multidict):
    regular_dict = {}
    for k in multidict.keys():
        v = multidict.getlist(k)
        regular_dict[k] = v if len(v) > 1 else v[0]
    return regular_dict


def snake_case_to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def map_grpc_request_params_to_dict(grpc_request):
    mapped_params = {}
    for field_descriptor, value in grpc_request.ListFields():
        name = snake_case_to_camel_case(field_descriptor.name)
        if isinstance(value, RepeatedScalarContainer):
            mapped_params[name] = []
            for v in value:
                if field_descriptor.enum_type is not None:
                    mapped_params[name].append(field_descriptor.enum_type.values_by_number[v].name)
                else:
                    mapped_params[name].append(v)
        else:
            mapped_params[name] = value
    return mapped_params


def map_content_to_api_spec(content):
    return {'results': content}
