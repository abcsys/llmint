from typing import Dict, Tuple, Generator, List


def read_mapping(input_data: Dict[str, List[Dict]]) -> Generator:
    """
    Generate samples from the given input_data. If allowed_kinds is provided,
    only those kinds will be used.

    Each sample contains 'kind', 'source', 'target', and 'mapping'.

    Parameters:
    - input_data: A dictionary with kinds as keys and lists of rows as values.

    Yields:
    - A dictionary containing 'kind', 'source', 'target', and 'mapping'.

    Each mapping is a dictionary containing 'from', 'to', and 'transformation'.
    """
    for kind, rows in input_data.items():
        for row in rows:
            yield {
                "kind": kind,
                "source": row["source"],
                "target": row["target"],
                "mapping": row["mapping"],
            }


def read_match(input_data: Dict[str, List[Dict]]) -> Generator:
    for kind, rows in input_data.items():
        for row in rows:
            yield {
                "kind": kind,
                "source": row["source"],
                "target": row["target"],
                "correspondence": [
                    {"from": mapping["from"],
                     "to": mapping["to"]}
                    for mapping in row["mapping"]
                ],
            }

def read_pt_match(input_data: Dict[str, List[Dict]]) -> Generator:
    for kind, rows in input_data.items():
        for row in rows:
            yield {
                "kind": kind,
                "source": row["source"],
                "target": row["target"],
                "correspondence": [mapping for mapping in row["mapping"]]
            }
