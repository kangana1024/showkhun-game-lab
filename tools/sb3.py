"""Read, write and diff-friendly dump of Scratch 3 .sb3 projects.

    python3 tools/sb3.py dump in.sb3 out.json
"""
import hashlib, json, sys, zipfile
from pathlib import Path


def read_project(sb3: Path) -> dict:
    with zipfile.ZipFile(sb3) as z:
        return json.loads(z.read("project.json"))


def dump_project(project: dict) -> str:
    """Stable JSON for git diffs: sorted keys, 2-space indent, Thai kept as is."""
    return json.dumps(project, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def asset(data: bytes, ext: str) -> dict:
    md5 = hashlib.md5(data).hexdigest()
    return {"assetId": md5, "md5ext": f"{md5}.{ext}", "dataFormat": ext}


def write_sb3(path: Path, project: dict, files: dict) -> None:
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("project.json", json.dumps(project, ensure_ascii=False))
        for name, data in files.items():
            z.writestr(name, data)


def sprite_opcodes(project: dict, sprite: str) -> list:
    for t in project["targets"]:
        if t["name"] == sprite:
            return sorted(b["opcode"] for b in t["blocks"].values() if isinstance(b, dict))
    raise KeyError(sprite)


if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[1] != "dump":
        raise SystemExit("usage: sb3.py dump in.sb3 out.json")
    Path(sys.argv[3]).write_text(dump_project(read_project(Path(sys.argv[2]))), encoding="utf-8")
