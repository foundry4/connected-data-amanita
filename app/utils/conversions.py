def lower_camel_case_to_upper(lower):
    return lower[0].upper() + lower[1:]


def map_multidict_to_dict(multidict):
    regular_dict = {}
    for k in multidict.keys():
        v = multidict.getlist(k)
        regular_dict[k] = v if len(v) > 1 else v[0]
    return regular_dict


# This function should be removed during the merge with 291
def lower_dict_keys(content):
    return {key.lower(): value for key, value in content.items()}


def map_content_to_api_spec(content):
    # [https://github.com/bbc/datalab-architecture/blob/master/api-specs/content-graph/content-graph.yml]
    # The next 4 lines should be removed during the merge with 291
    new_content = []
    for item in content:
        new_item = lower_dict_keys(item)
        new_content.append(new_item)
    return {'results': new_content}
