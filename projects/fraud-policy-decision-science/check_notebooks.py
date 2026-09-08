"""Execute each walkthrough in a fresh namespace using the installed package."""

import json
import os
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    os.chdir(root / "notebooks")
    for notebook in sorted(Path.cwd().glob("*.ipynb")):
        namespace = {"__name__": "__main__"}
        document = json.loads(notebook.read_text())
        for index, cell in enumerate(document["cells"]):
            if cell["cell_type"] == "code":
                code = "".join(cell["source"])
                exec(compile(code, f"{notebook.name}:cell-{index}", "exec"), namespace)
        print(f"PASS: {notebook.name}", flush=True)


if __name__ == "__main__":
    main()
