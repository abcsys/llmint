from typing import Dict, Tuple, Generator, List


def read_corresp(input_data: Dict[str, List[Dict]],
                 match_only: bool = False) -> Generator:
    """
    Generate samples from the given input_data. If allowed_kinds is provided,
    only those kinds will be used.

    Each sample contains 'kind', 'source', 'target', and 'correspondence'.

    Parameters:
    - input_data: A dictionary with kinds as keys and lists of rows as values.

    Yields:
    - A dictionary containing 'kind', 'source', 'target', and 'correspondence'.
    """
    for kind, rows in input_data.items():
        for row in rows:
            yield {
                "kind": kind,
                "source": row["source"],
                "target": row["target"],
                "correspondence": row["correspondence"],
            }


def match_only(correspondence: Dict):
    """
    Keep only match in a correspondence.
    """
    return {
        "from": correspondence["from"],
        "to": correspondence["to"],
    }
