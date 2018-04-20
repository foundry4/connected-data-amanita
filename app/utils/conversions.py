"""Functions to map/convert simple data."""


def lower_camel_case_to_upper(lower):
    return lower[0].upper() + lower[1:]


def map_multidict_to_dict(multidict):
    regular_dict = {}
    for k in multidict.keys():
        v = multidict.getlist(k)
        regular_dict[k] = v if len(v) > 1 else v[0]
    return regular_dict


def map_content_to_api_spec(content):
    # [https://github.com/bbc/datalab-architecture/blob/master/api-specs/content-graph/content-graph.yml]
    return {'Results': content}
