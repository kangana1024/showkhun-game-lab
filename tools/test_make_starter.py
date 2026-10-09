import hashlib, tempfile, unittest, zipfile
from pathlib import Path
from PIL import Image, ImageDraw
import make_starter, sb3

BG = (226, 223, 219)


def fake_sheet():
    im = Image.new("RGB", (200, 300), BG)
    ImageDraw.Draw(im).ellipse([50, 50, 150, 250], fill=(180, 100, 40), outline=(0, 0, 0), width=4)
    return im


class StarterTest(unittest.TestCase):
    def test_cutout_clears_background_and_keeps_subject(self):
        dog = make_starter.cutout(fake_sheet(), 120)
        self.assertEqual(dog.height, 120)
        self.assertEqual(dog.getpixel((0, 0))[3], 0)
        self.assertEqual(dog.getpixel((dog.width // 2, 60))[3], 255)

    def test_build_writes_consistent_project(self):
        with tempfile.TemporaryDirectory() as d:
            sheet, out = Path(d) / "sheet.png", Path(d) / "starter.sb3"
            fake_sheet().save(sheet)
            make_starter.build(sheet, out)
            p = sb3.read_project(out)
            z = zipfile.ZipFile(out)
            self.assertEqual([t["name"] for t in p["targets"]], ["Stage", "หยองหยอง"])
            for t in p["targets"]:
                self.assertEqual(t["blocks"], {})
                for c in t["costumes"]:
                    self.assertEqual(hashlib.md5(z.read(c["md5ext"])).hexdigest(), c["assetId"])
                    self.assertEqual(c["bitmapResolution"], 2)
            st = p["targets"][0]["costumes"][0]
            self.assertEqual((st["rotationCenterX"], st["rotationCenterY"]), (480, 360))
            self.assertEqual(p["targets"][1]["rotationStyle"], "all around")


if __name__ == "__main__":
    unittest.main()
