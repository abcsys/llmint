from typing import Dict, Set, Generator, List


def read_corresp(input_data: Dict[str, List[Dict]],
                 allowed_kinds: Set[str] = None) -> Generator:
    """
    Generate samples from the given input_data. If allowed_kinds is provided,
    only those kinds will be used.

    Each sample contains 'kind', 'source', 'target', and 'correspondence'.

    Parameters:
    - input_data: A dictionary with kinds as keys and lists of rows as values.
    - allowed_kinds: A set of kinds to be used for generating samples.

    Yields:
    - A dictionary containing 'kind', 'source', 'target', and 'correspondence'.
    """
    for kind, rows in input_data.items():
        if allowed_kinds and kind not in allowed_kinds:
            continue
        for row in rows:
            yield {
                "kind": kind,
                "source": row["source"],
                "target": row["target"],
                "correspondence": row["correspondence"],
            }
