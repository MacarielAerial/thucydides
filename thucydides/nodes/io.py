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
    if path_jsonl.is_file():
        log.warning(
            f"{path_jsonl} already exists as a file. "
            f"Deleting it before replacing it with the result of the current run"
        )
        path_jsonl.unlink()

    with open(path_jsonl, "w") as f:
        for a_json in output_jsonl:
            json.dump(a_json, f)
            f.write("\n")

    log.info(
        f"Concatenated {len(output_jsonl)} JSON files "
        f"and exported the result to {path_jsonl}"
    )


if __name__ == "__main__":
    """
    Example usage:
    pipenv run python -m thucydides.nodes.io \
    -jsons data/01_raw/news-articles/ \
    -jsonl data/02_intermediate/news-articles.jsonl
    """
    import argparse
    import logging

    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-jsons",
        "--path_dir_json",
        type=Path,
        help="Path to the directory with news article json files",
        required=True,
    )
    parser.add_argument(
        "-jsonl",
        "--path_jsonl",
        type=Path,
        help="Path to the jsonl file that will be created",
        required=True,
    )

    args = parser.parse_args()

    paths_json: List[Path] = list(args.path_dir_json.iterdir())
    jsons_to_jsonl(paths_json=paths_json, path_jsonl=args.path_jsonl)
