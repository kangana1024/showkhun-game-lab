import subprocess, sys, tempfile, unittest
from pathlib import Path
import rbxlx

PLACE = """<roblox version="4">
<Item class="Workspace" referent="RBX0"><Properties><string name="Name">Workspace</string></Properties>
 <Item class="Part" referent="RBX1"><Properties><bool name="Anchored">false</bool><string name="Name">Part</string></Properties>
  <Item class="Script" referent="RBX2"><Properties><string name="Name">Script</string>
   <ProtectedString name="Source"><![CDATA[while true do
	script.Parent.Brickcolor = BrickColor.random()
end]]></ProtectedString></Properties></Item>
 </Item>
 <Item class="Part" referent="RBX3"><Properties><bool name="Anchored">true</bool><string name="Name">Part</string></Properties></Item>
 <Item class="SpawnLocation" referent="RBX5"><Properties><bool name="Anchored">true</bool><string name="Name">SpawnLocation</string></Properties></Item>
</Item>
<Item class="Lighting" referent="RBX4"><Properties><string name="Name">Lighting</string></Properties></Item>
</roblox>"""

TOOL = Path(__file__).resolve().parent / "rbxlx.py"


class RbxlxTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.place = Path(self.tmp.name) / "p.rbxlx"
        self.place.write_text(PLACE, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_parts_lists_only_part_class_with_anchored(self):
        self.assertEqual(rbxlx.parts(rbxlx.load(self.place)),
                         [{"path": "Workspace/Part", "anchored": False},
                          {"path": "Workspace/Part", "anchored": True}])

    def test_scripts_have_path_class_and_source(self):
        s = rbxlx.scripts(rbxlx.load(self.place))
        self.assertEqual(len(s), 1)
        self.assertEqual(s[0]["path"], "Workspace/Part/Script")
        self.assertEqual(s[0]["cls"], "Script")
        self.assertIn("script.Parent.Brickcolor = BrickColor.random()", s[0]["source"])

    def test_cli_script_prints_source_with_trailing_newline(self):
        out = subprocess.run([sys.executable, str(TOOL), "script", str(self.place)],
                             capture_output=True, text=True, check=True).stdout
        self.assertTrue(out.startswith("while true do\n"))
        self.assertTrue(out.endswith("end\n"))

    def test_cli_script_fails_without_exactly_one_script(self):
        empty = Path(self.tmp.name) / "e.rbxlx"
        empty.write_text('<roblox version="4"></roblox>', encoding="utf-8")
        r = subprocess.run([sys.executable, str(TOOL), "script", str(empty)], capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("exactly one Script", r.stderr)


if __name__ == "__main__":
    unittest.main()
