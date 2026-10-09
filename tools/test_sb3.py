import json, tempfile, unittest, zipfile
from pathlib import Path
import sb3


class Sb3Test(unittest.TestCase):
    def test_asset_uses_md5_of_bytes(self):
        a = sb3.asset(b"abc", "png")
        self.assertEqual(a["assetId"], "900150983cd24fb0d6963f7d28e17f72")
        self.assertEqual(a["md5ext"], "900150983cd24fb0d6963f7d28e17f72.png")
        self.assertEqual(a["dataFormat"], "png")

    def test_roundtrip_and_stable_dump(self):
        p = {"targets": [{"name": "หยองหยอง", "blocks": {"b": {"opcode": "motion_changexby"}}}], "meta": {"semver": "3.0.0"}}
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "t.sb3"
            sb3.write_sb3(f, p, {"x.png": b"1"})
            self.assertEqual(sb3.read_project(f), p)
            self.assertIn("x.png", zipfile.ZipFile(f).namelist())
        once = sb3.dump_project(p)
        self.assertEqual(once, sb3.dump_project(json.loads(once)))
        self.assertIn("หยองหยอง", once)

    def test_sprite_opcodes_skips_array_blocks(self):
        p = {"targets": [{"name": "s", "blocks": {"a": {"opcode": "event_whenflagclicked"}, "v": [12, "x", "id", 0, 0]}}]}
        self.assertEqual(sb3.sprite_opcodes(p, "s"), ["event_whenflagclicked"])


if __name__ == "__main__":
    unittest.main()
