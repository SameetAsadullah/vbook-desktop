#!/usr/bin/env python3
"""Run lightweight structural checks for the VBook repository."""

from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    ROOT / "README.md",
    ROOT / "LICENSE",
    ROOT / "source-code/src/presentationLayer/Main.java",
]
FORBIDDEN_PARTS = ("source-code/out/", "source-code/.idea/", "requirements/")
FORBIDDEN_SUFFIXES = (".class", ".iml", ".rar")


def tracked_files() -> list[str]:
    output = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True)
    return output.splitlines()


def validate_readme_links() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    targets = re.findall(r"!\[[^]]*\]\(([^)]+)\)", readme)
    local_targets = [target for target in targets if not target.startswith(("http://", "https://"))]
    missing = [target for target in local_targets if not (ROOT / target).is_file()]
    if missing:
        raise SystemExit(f"Missing README images: {', '.join(missing)}")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required files: {', '.join(missing)}")

    tracked = tracked_files()
    forbidden = [
        path
        for path in tracked
        if path.endswith(FORBIDDEN_SUFFIXES)
        or any(part in path for part in FORBIDDEN_PARTS)
    ]
    if forbidden:
        raise SystemExit("Generated files are tracked:\n" + "\n".join(forbidden))

    fxml_files = sorted(ROOT.glob("source-code/src/**/*.fxml"))
    for path in fxml_files:
        ET.parse(path)

    validate_readme_links()
    java_count = len(list(ROOT.glob("source-code/src/**/*.java")))
    print(f"Validated {java_count} Java files and {len(fxml_files)} FXML views.")


if __name__ == "__main__":
    main()
