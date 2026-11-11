#!/usr/bin/env python3
"""Execute a Jupyter notebook without importing Jupyter.

Code cells run in order in one shared namespace. Standard output and standard
error are captured as stream outputs. By default, the tracked input notebook is
left unchanged and the executed result is written beside it with an
``.executed.ipynb`` suffix.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import sys
import traceback
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Inputs:
        Command-line arguments supplied through ``sys.argv``.

    Returns:
        argparse.Namespace: Resolved input notebook and optional output path.
    """
    parser = argparse.ArgumentParser(
        description="Execute all code cells and save an executed notebook copy."
    )
    parser.add_argument("notebook", type=Path, help="Input .ipynb file")
    parser.add_argument(
        "--output",
        type=Path,
        help="Output .ipynb path; defaults to NAME.executed.ipynb",
    )
    return parser.parse_args()


def output_path_for(input_path: Path, requested: Path | None) -> Path:
    """Choose the executed-notebook destination.

    Inputs:
        input_path: Resolved input notebook path.
        requested: User-provided output path, or ``None``.

    Returns:
        pathlib.Path: Absolute output path.
    """
    if requested is not None:
        return requested.resolve()
    return input_path.with_name(f"{input_path.stem}.executed.ipynb")


def stream_output(text: str) -> dict:
    """Build one Jupyter stream-output object.

    Inputs:
        text: Captured standard output and standard error.

    Returns:
        dict: Notebook-compatible stream output.
    """
    return {
        "output_type": "stream",
        "name": "stdout",
        "text": text.splitlines(keepends=True),
    }


def main() -> int:
    """Execute the notebook and return a process exit status.

    Inputs:
        Parsed command-line paths and the notebook JSON document.

    Returns:
        int: Zero on success and one after a failed code cell.
    """
    args = parse_args()
    notebook_path = args.notebook.resolve()
    output_path = output_path_for(notebook_path, args.output)

    if notebook_path.suffix.lower() != ".ipynb":
        raise ValueError(f"expected an .ipynb file: {notebook_path}")
    if not notebook_path.is_file():
        raise FileNotFoundError(notebook_path)

    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    namespace: dict[str, object] = {"__name__": "__main__"}
    code_count = 0

    # Relative input paths and project-root discovery should behave as they do
    # when a user launches Jupyter from the notebook directory.
    previous_directory = Path.cwd()
    os.chdir(notebook_path.parent)
    try:
        for cell_index, cell in enumerate(notebook["cells"]):
            if cell.get("cell_type") != "code":
                continue

            code_count += 1
            source = "".join(cell.get("source", []))
            captured = io.StringIO()
            try:
                with redirect_stdout(captured), redirect_stderr(captured):
                    exec(
                        compile(source, f"{notebook_path.name}:cell-{cell_index}", "exec"),
                        namespace,
                    )
            except Exception:
                captured.write("\n")
                captured.write(traceback.format_exc())
                cell["outputs"] = [stream_output(captured.getvalue())]
                cell["execution_count"] = code_count
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(
                    json.dumps(notebook, indent=1, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )
                print(
                    f"[FAIL] code cell {code_count}; partial output written to {output_path}",
                    file=sys.stderr,
                )
                print(captured.getvalue(), file=sys.stderr)
                return 1

            text = captured.getvalue()
            cell["outputs"] = [stream_output(text)] if text else []
            cell["execution_count"] = code_count
            print(f"--- code cell {code_count} ---")
            if text:
                print(text, end="" if text.endswith("\n") else "\n")
    finally:
        os.chdir(previous_directory)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(notebook, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"executed {code_count} code cells; output written to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
