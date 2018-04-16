def build_sort_statement(sort_fields):
    query = []
    if sort_fields:
        for field in sort_fields:
            if field[0] == '-':
                order = 'desc'
                field = field[1:]
            else:
                order = 'asc'
                field = field
            query.append({field:order})
    return query


def build_filter_body(filter_type, key, val):
    filter_body = {
        filter_type: {
            key: val
        }
    }
    return filter_body


def build_must_body(must_type, key, val):
    must_body = {
        must_type: {
            key: val
        }
    }
    return must_body


def update_dict_recursively(d, path, value, val_is_list=False):
    """Non-destructively update a dict, if a list exists already then append to list."""
    if len(path) == 1:
        if path[0] in d:
            existing_val = d[path[0]]
            if val_is_list and not isinstance(existing_val, list):
                raise ValueError('Value specified as list but dict already contains non-list value.')
            elif not val_is_list and isinstance(existing_val,list):
                raise ValueError('Value specified as non-list but dict already contains list value.')
            elif isinstance(existing_val, list) and val_is_list:
                if isinstance(value, list):
                    d[path[0]].extend(value)
                else:
                    d[path[0]].append(value)
        else:
            if (val_is_list and isinstance(value, list)) or (not val_is_list and not isinstance(value, list)):
                d[path[0]] = value
            elif val_is_list and not isinstance(value, list):
                d[path[0]] = [value]
            else:
                d[path]
    else:
        d.setdefault(path[0], {})
        update_dict_recursively(d[path[0]], path[1:], value)

    return d


def build_bool_queries(queries):
    res = []
    for item in queries:
        res.append({
            item[0]: {
                item[1]: item[2]
            }
        })
    return res
