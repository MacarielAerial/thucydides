import json
import logging
from pathlib import Path
from typing import Any, Dict, List

log = logging.getLogger(__name__)


def jsons_to_jsonl(paths_json: List[Path], path_jsonl: Path) -> None:
    """Concatenates multiple jsons into one single jsonl
    before dumping the result to {path_jsonl}"""
    # Load jsons into a list of python dictionaries
    output_jsonl: List[Dict[str, Any]] = []
    for path_json in paths_json:
        with open(path_json, "r") as f:
            a_json = json.load(f)
            output_jsonl.append(a_json)

    # Write these python dictionaries into one single file
    with open(path_jsonl, "w") as f:
        for a_json in output_jsonl:
            json.dump(a_json, f)
            f.write("\n")

    log.info(
        f"Concatenated {len(output_jsonl)} JSON files "
        f"and exported the result to {path_jsonl}"
    )
