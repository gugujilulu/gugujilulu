"""Check publishable figures, local links, source fingerprints and explorer grid."""

import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image


def main():
    root = Path(__file__).resolve().parent
    errors = []
    for p in (root / "results/figures").glob("*.svg"):
        ET.parse(p)
    for p in (root / "results/figures").glob("*.png"):
        with Image.open(p) as im:
            im.verify()
    documents = list(root.glob("*.md"))
    for folder in ["docs", "notebooks", "data/case_inputs"]:
        documents.extend((root / folder).rglob("*.md"))
    for p in documents:
        for target in re.findall(r"\]\(([^)]+)\)", p.read_text()):
            target = target.split("#")[0]
            if target and "://" not in target and not (p.parent / target).exists():
                errors.append(f"{p.relative_to(root)}: broken link {target}")
    manifest = json.loads((root / "results/manifest.json").read_text())
    for name, expected in manifest.items():
        actual = hashlib.sha256((root / name).read_bytes()).hexdigest()
        if actual != expected:
            errors.append(f"Manifest mismatch: {name}")
    html = (root / "reports/policy_explorer.html").read_text()
    grid = json.loads(re.search(r"const GRID=(.*?);\n", html).group(1))
    assert len(grid) == 135
    assert all(len(v["backlog"]) == 84 for v in grid.values())
    assert len(list((root / "results/figures").glob("*.svg"))) == 13
    if errors:
        raise RuntimeError("\n".join(errors))
    print(
        "PASS: 13 SVGs, available PNGs, local links, manifest and 135 explorer scenarios"
    )


if __name__ == "__main__":
    main()
