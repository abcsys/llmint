def diff_dicts(dict1, dict2):
    """Returns the difference between two dictionaries."""
    diffs = {}
    for key, value in dict1.items():
        if key not in dict2 or dict2[key] != value:
            diffs[key] = (value, dict2.get(key))
    return diffs


def diff_lists(list1, list2):
    """Returns the difference between two lists of dictionaries."""
    diffs = []
    for d1, d2 in zip(list1, list2):
        diff = diff_dicts(d1, d2)
        if diff:
            diffs.append(diff)
    return diffs


diff_corresp = diff_lists
