"""Functions to map/convert simple data."""


def map_multidict_to_dict(multidict):
    regular_dict = {}
    for k in multidict.keys():
        v = multidict.getlist(k)
        regular_dict[k] = v if len(v) > 1 else v[0]
    return regular_dict


def map_content_to_api_spec(content):
    return {'results': content}
