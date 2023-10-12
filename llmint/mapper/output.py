def _parse_dict_str(dict_str):
    # Manually parse the dictionary string
    dict_content = {}
    key_value_pairs = dict_str[1:-1].split(", ")
    for pair in key_value_pairs:
        # Find the first occurrence of ': ' to split
        split_index = pair.find(": ")
        key = pair[:split_index].strip("'")
        value = pair[split_index + 2:].strip("'")
        dict_content[key] = value
    return dict_content


def format_output(data):
    result = []
    current_item = {}
    inside_dict = False
    dict_str = ""

    for item in data:
        if item.endswith("'}"):
            inside_dict = False
            dict_str += ", " + item
            current_item['transformation'] = _parse_dict_str(dict_str)
            dict_str = ""
            result.append(current_item)
            current_item = {}
        elif inside_dict:
            dict_str += ", " + item
        else:
            pos = item.find(': ')
            key = item[:pos].strip("'")
            value = item[pos + 2:].strip("'")

            if value.startswith('{'):
                inside_dict = True
                dict_str = value
            else:
                current_item[key] = value
                if key == 'transformation':
                    result.append(current_item)
                    current_item = {}

    return result


def _diff_dicts(dict1, dict2):
    """Returns the difference between two dictionaries."""
    diffs = {}
    for key, value in dict1.items():
        if key not in dict2 or dict2[key] != value:
            diffs[key] = (value, dict2.get(key))
    return diffs


def _diff_lists(list1, list2):
    """Returns the difference between two lists of dictionaries."""
    diffs = []
    for d1, d2 in zip(list1, list2):
        diff = _diff_dicts(d1, d2)
        if diff:
            diffs.append(diff)
    return diffs


def diff_mapping(true, pred):
    try:
        return _diff_lists(true, pred)
    except:
        return true


def test_format_output():
    # Sample data
    data = ["'from': 'power", "to': 'power", "transformation': {'inactive': 'active", "active': 'active'}",
            "'from': 'light_percent", "to': 'brightness", "transformation': 'X / 100.0'"]
    print(format_output(data))


if __name__ == '__main__':
    test_format_output()
