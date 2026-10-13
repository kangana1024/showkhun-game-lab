"""Read Roblox .rbxlx place files (XML): parts and script sources.

    python3 tools/rbxlx.py script place.rbxlx     print the only Script's Source
"""
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SCRIPT_CLASSES = ("Script", "LocalScript", "ModuleScript")


def load(path):
    return ET.parse(path).getroot()


def _prop(item, tag, name):
    props = item.find("Properties")
    if props is None:
        return None
    for el in props.findall(tag):
        if el.get("name") == name:
            return el.text or ""
    return None


def _walk(item, prefix):
    name = _prop(item, "string", "Name") or item.get("class")
    path = f"{prefix}/{name}" if prefix else name
    yield item, path
    for child in item.findall("Item"):
        yield from _walk(child, path)


def _items(root):
    for top in root.findall("Item"):
        yield from _walk(top, "")


def parts(root):
    return [{"path": p, "anchored": _prop(it, "bool", "Anchored") == "true"}
            for it, p in _items(root) if it.get("class") == "Part"]


def scripts(root):
    return [{"path": p, "cls": it.get("class"), "source": _prop(it, "ProtectedString", "Source") or ""}
            for it, p in _items(root) if it.get("class") in SCRIPT_CLASSES]


def main(argv):
    if len(argv) != 3 or argv[1] != "script":
        sys.exit("usage: rbxlx.py script place.rbxlx")
    found = [s for s in scripts(load(Path(argv[2]))) if s["cls"] == "Script"]
    if len(found) != 1:
        sys.exit(f"expected exactly one Script, found {len(found)}")
    src = found[0]["source"]
    sys.stdout.write(src if src.endswith("\n") else src + "\n")


if __name__ == "__main__":
    main(sys.argv)
