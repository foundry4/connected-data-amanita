def build_sort_statement(sort_fields):
    query = {}
    if sort_fields:
        for field in sort_fields:
            if field[0] == '-':
                order = 'desc'
                field = field[1:]
            else:
                order = 'asc'
                field = field
            query[field] = order
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


def update_dict_recursively(d, path, value):
    if len(path) == 1:
        d[path[0]] = value
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
