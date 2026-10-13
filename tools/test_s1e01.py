import unittest
from pathlib import Path
import sb3

EP = Path(__file__).resolve().parent.parent / "scratch" / "s1e01-move"


def ops(name):
    return sb3.sprite_opcodes(sb3.read_project(EP / f"{name}.sb3"), "หยองหยอง")


class S1E01Test(unittest.TestCase):
    """Each saved state really contains its bug, and fix.sb3 really contains every fix."""

    def test_bug1_noloop_has_no_forever(self):
        o = ops("bug-noloop")
        self.assertIn("motion_changexby", o)
        self.assertIn("sensing_keypressed", o)
        self.assertNotIn("control_forever", o)

    def test_bug2_flip_turns_without_rotation_style(self):
        o = ops("bug-flip")
        self.assertIn("control_forever", o)
        self.assertIn("motion_pointindirection", o)
        self.assertNotIn("motion_setrotationstyle", o)

    def test_bug3_edge_has_no_clamp(self):
        o = ops("bug-edge")
        self.assertIn("motion_setrotationstyle", o)
        self.assertNotIn("motion_setx", o)

    def test_fix_has_loop_rotation_style_and_clamp(self):
        o = ops("fix")
        for op in ("control_forever", "motion_setrotationstyle", "motion_setx", "operator_gt", "operator_lt"):
            self.assertIn(op, o)


if __name__ == "__main__":
    unittest.main()
