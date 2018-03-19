def compare_dictionaries(dict_1, dict_2, dict_1_name, dict_2_name, path=""):
    """Compare two dictionaries recursively to find non mathcing elements

    Args:
        dict_1: dictionary 1
        dict_2: dictionary 2

    Returns:

    """
    err = ''
    key_err = ''
    value_err = ''
    old_path = path
    for k in dict_1.keys():
        path = old_path + "[%s]" % k
        if k not in dict_2:
            key_err += "Key %s%s not in %s\n" % (dict_2_name, path, dict_2_name)
        else:
            if isinstance(dict_1[k], dict) and isinstance(dict_2[k], dict):
                comp, _ = compare_dictionaries(dict_1[k], dict_2[k], dict_1_name, dict_2_name, path)
                err += comp
            elif isinstance(dict_1[k], list) and isinstance(dict_2[k], list):
                for item1, item2 in zip(order_list_of_dicts(dict_1[k]), order_list_of_dicts(dict_2[k])):
                    if isinstance(item1, dict) and isinstance(item2, dict):
                        comp, _ = compare_dictionaries(item1, item2, dict_1_name, dict_2_name, path)
                        err += comp
                    else:
                        value_err += "Value of %s%s (%s) not same as %s%s (%s)\n" \
                                     % (dict_1_name, path, item1, dict_2_name, path, item2)

            else:
                if dict_1[k] != dict_2[k]:
                    value_err += "Value of %s%s (%s) not same as %s%s (%s)\n" \
                                 % (dict_1_name, path, dict_1[k], dict_2_name, path, dict_2[k])

    for k in dict_2.keys():
        path = old_path + "[%s]" % k
        if k not in dict_1:
            key_err += "Key %s%s not in %s\n" % (dict_2_name, path, dict_1_name)
    err_str = key_err + value_err + err
    is_same = True if err_str == '' else False
    return err_str, is_same


def order_list_of_dicts(lst):
    return sorted(lst, key=lambda k: str(k.values()))
