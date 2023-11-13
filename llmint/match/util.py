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


def diff_corresp(true, pred):
    try:
        return diff_lists(true, pred)
    except:
        return true


def format_output(raw_output):
    """Convert the prediction format to match the desired ground-truth format."""
    # Split strings by ': ' to get key-value pairs
    split_pairs = [item.split(": ")[1].strip("'") for item in raw_output]
    # Create dictionaries in pairs of two items
    return [{'from': split_pairs[i], 'to': split_pairs[i + 1]} for i in range(0, len(split_pairs), 2)]

def pt_format_output(raw_output):
    """Convert the prediction format to match the desired ground-truth format."""
    # Clean brackets and quotes, split into `from` and `to` of the form 
    # [['from: key1'], ['to: value1'], ['transformation: t1']... ['from: keyn], ['to: valuen], ['transformation: tn']]
    clean_output = [item.replace("{ ", "").replace(" }", "").split(", ") for item in raw_output]
    # Split strings by ': ' to get key-values of the form 
    # [key1, value1, t1, key2, value2, t2, ..., keyn, valuen, tn]
    split_pairs = [item[0].split(": ")[1].strip('"').strip("'") for item in clean_output]
    # Create dictionaries in pairs of two items
    return [{'from': split_pairs[i], 'to': split_pairs[i + 1]} for i in range(0, len(split_pairs), 3)]

def pt_format_input(raw_input):
    """Convert the input format to match the desired ground-truth format."""
    # Clean brackets and quotes, split into `from` and `to` pairs
    clean_input = [item.replace("{{ ", "").replace(" }}", "").split(", ") for item in raw_input]
    # Split strings by ': ' to get key-value pairs
    split_pairs = [ [item.split(": ")[1].strip('"').strip("'") for item in i] for i in clean_input]
    # Create dictionaries in pairs of two items
    return [{'from': split_pairs[i][0], 'to': split_pairs[i][1]} for i in range(0, len(split_pairs))]
