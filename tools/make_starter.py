"""Build a Scratch starter project: หยองหยอง sprite on a drawn park backdrop, no scripts.

    python3 tools/make_starter.py <yong-yong sheet.png> scratch/s1e01-move/starter.sb3
"""
import sys
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageDraw
import sb3

STAGE_W, STAGE_H, RES = 480, 360, 2  # bitmapResolution 2: images are drawn at 2x stage pixels


def cutout(sheet, height, tol=30):
    """Flood-fill the flat sheet background from the four corners, crop to the subject, scale to `height` px."""
    im = sheet.convert("RGBA")
    w, h = im.size
    for xy in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        ImageDraw.floodfill(im, xy, (0, 0, 0, 0), thresh=tol)
    im = im.crop(im.getbbox())
    return im.resize((round(im.width * height / im.height), height), Image.LANCZOS)


def backdrop():
    """Sky gradient over grass, drawn in code so the repo carries no third-party art."""
    w, h = STAGE_W * RES, STAGE_H * RES
    im = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(im)
    for y in range(h):
        k = y / h
        d.line([(0, y), (w, y)], fill=(int(140 + 80 * k), int(200 + 40 * k), 255))
    g = int(h * 0.72)
    d.rectangle([0, g, w, h], fill=(120, 190, 90))
    d.rectangle([0, g, w, g + 10], fill=(95, 165, 70))
    return im


def png(im):
    b = BytesIO()
    im.save(b, "PNG", optimize=True)
    return b.getvalue()


def costume(name, data, size):
    c = sb3.asset(data, "png")
    c.update(name=name, bitmapResolution=RES, rotationCenterX=size[0] // 2, rotationCenterY=size[1] // 2)
    return c


def target(name, costume_, is_stage):
    t = {"isStage": is_stage, "name": name, "variables": {}, "lists": {}, "broadcasts": {}, "blocks": {},
         "comments": {}, "currentCostume": 0, "costumes": [costume_], "sounds": [], "volume": 100,
         "layerOrder": 0 if is_stage else 1}
    if is_stage:
        t.update(tempo=60, videoTransparency=50, videoState="on", textToSpeechLanguage=None)
    else:
        t.update(visible=True, x=0, y=-95, size=100, direction=90, draggable=False, rotationStyle="all around")
    return t


def build(sheet_path, out, sprite_name="หยองหยอง", sprite_h=240):
    dog, bg = cutout(Image.open(sheet_path), sprite_h), backdrop()
    dog_png, bg_png = png(dog), png(bg)
    sc, dc = costume("สวนสาธารณะ", bg_png, bg.size), costume("นั่ง", dog_png, dog.size)
    project = {"targets": [target("Stage", sc, True), target(sprite_name, dc, False)],
               "monitors": [], "extensions": [],
               "meta": {"semver": "3.0.0", "vm": "0.2.0", "agent": "showkhun-game-lab make_starter.py"}}
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    sb3.write_sb3(Path(out), project, {sc["md5ext"]: bg_png, dc["md5ext"]: dog_png})


if __name__ == "__main__":
    build(Path(sys.argv[1]), Path(sys.argv[2]))
