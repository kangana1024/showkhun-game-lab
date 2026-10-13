import unittest
from pathlib import Path
import rbxlx

EP = Path(__file__).resolve().parent.parent / "roblox" / "s2e01-blink"


def state(name):
    root = rbxlx.load(EP / f"{name}.rbxlx")
    src = [s["source"] for s in rbxlx.scripts(root) if s["cls"] == "Script"]
    return rbxlx.parts(root), src


class S2E01Test(unittest.TestCase):
    """Each saved state really contains its bug, and fix.rbxlx contains every fix."""

    def test_bug1_fall_parts_not_anchored_and_no_script(self):
        parts, src = state("bug-fall")
        self.assertEqual(len(parts), 3)
        self.assertTrue(all(not p["anchored"] for p in parts))
        self.assertEqual(src, [])

    def test_bug2_typo_anchored_with_lowercase_c(self):
        parts, src = state("bug-typo")
        self.assertTrue(all(p["anchored"] for p in parts))
        self.assertEqual(len(src), 1)
        self.assertIn("part.Brickcolor = BrickColor.random()", src[0])
        self.assertNotIn("wait", src[0])

    def test_bug3_timeout_fixed_typo_but_no_wait(self):
        _, src = state("bug-timeout")
        self.assertIn("part.BrickColor = BrickColor.random()", src[0])
        self.assertNotIn("Brickcolor", src[0])
        self.assertNotIn("wait", src[0])

    def test_fix_has_wait_and_correct_property(self):
        parts, src = state("fix")
        self.assertTrue(all(p["anchored"] for p in parts))
        self.assertIn("part.BrickColor = BrickColor.random()", src[0])
        self.assertIn("task.wait(0.5)", src[0])

    def test_luau_copy_matches_fix_state(self):
        _, src = state("fix")
        self.assertEqual((EP / "Blink.server.luau").read_text(encoding="utf-8").rstrip("\n"), src[0].rstrip("\n"))


if __name__ == "__main__":
    unittest.main()
