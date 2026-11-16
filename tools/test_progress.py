import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

import progress


class ProgressTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "tracking.json"

    def cli(self, *args):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return progress.main(["--file", str(self.path), *args])

    def test_complete_and_undo_invalidates_acceptance(self):
        self.assertEqual(self.cli("accept", "1"), 1)
        for lab in ("W01-L1", "W01-L2", "W01-L3"):
            self.assertEqual(self.cli("done", lab), 0)
        self.assertEqual(self.cli("accept", "1"), 0)
        self.assertTrue(progress.read(self.path)["weeks"]["1"]["accepted"])
        self.assertEqual(self.cli("undo", "W01-L2"), 0)
        state = progress.read(self.path)["weeks"]["1"]
        self.assertFalse(state["accepted"])
        self.assertEqual(state["labs"], [True, False, True])

    def test_merge_keeps_both_devices_but_replace_preserves_unchecks(self):
        self.cli("done", "W01-L1")
        incoming = progress.empty()
        incoming["weeks"]["2"]["labs"][2] = True
        other = self.path.parent / "from-other-device.json"
        progress.write(other, incoming)
        self.assertEqual(self.cli("import", str(other)), 0)
        self.assertTrue(progress.read(self.path)["weeks"]["1"]["labs"][0])
        self.assertTrue(progress.read(self.path)["weeks"]["2"]["labs"][2])
        self.assertEqual(self.cli("import", str(other), "--replace"), 0)
        self.assertFalse(progress.read(self.path)["weeks"]["1"]["labs"][0])

    def test_invalid_import_does_not_modify_existing_file(self):
        self.cli("done", "W01-L1")
        original = self.path.read_bytes()
        invalid = self.path.parent / "invalid.json"
        invalid.write_text('{"version": 1, "weeks": {"1": {"labs": ["yes", false, false]}}}')
        self.assertEqual(self.cli("import", str(invalid)), 1)
        self.assertEqual(self.path.read_bytes(), original)

    def test_export_and_reload_match_browser_format(self):
        self.cli("done", "W32-L3")
        exported = self.path.parent / "export.json"
        self.assertEqual(self.cli("export", str(exported)), 0)
        data = json.loads(exported.read_text())
        self.assertEqual(data["version"], 1)
        self.assertEqual(len(data["weeks"]), 32)
        self.assertEqual(data["weeks"]["32"]["labs"], [False, False, True])


if __name__ == "__main__":
    unittest.main()
