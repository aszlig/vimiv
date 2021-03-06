#!/usr/bin/env python
# encoding: utf-8
"""Completion tests for vimiv's test suite."""

from unittest import TestCase, main
import vimiv.main as v_main
from vimiv.parser import parse_config


class CompletionsTest(TestCase):
    """Completions Tests."""

    @classmethod
    def setUpClass(cls):
        cls.settings = parse_config()
        cls.vimiv = v_main.Vimiv(cls.settings, [], 0)
        cls.vimiv.main()

    def test_reset(self):
        """Reset the internal completion values."""
        self.vimiv.commandline.entry.set_text(":a")
        self.vimiv.completions.complete()
        self.vimiv.completions.reset()
        self.assertEqual(self.vimiv.completions.tab_presses, 0)
        self.assertFalse(self.vimiv.completions.cycling)
        self.assertEqual(self.vimiv.completions.completions, [])
        self.assertEqual(self.vimiv.completions.compstr, "")

    def test_internal_completion(self):
        """Completion of internal commands."""
        self.vimiv.commandline.entry.set_text(":a")
        self.vimiv.completions.complete()
        expected_completions = ["accept_changes", "alias", "autorotate"]
        self.assertEqual(self.vimiv.completions.completions,
                         expected_completions)

    def test_external_completion(self):
        """Completion of external commands."""
        self.vimiv.commandline.entry.set_text(":!vimi")
        self.vimiv.completions.complete()
        expected_completions = ["!vimiv"]
        self.assertEqual(self.vimiv.completions.completions,
                         expected_completions)

    def test_external_with_path_completion(self):
        """Completion of external commands."""
        self.vimiv.commandline.entry.set_text(":!ls vimi")
        self.vimiv.completions.complete()
        expected_completions = ["!ls vimiv/"]
        self.assertEqual(self.vimiv.completions.completions,
                         expected_completions)

    def test_path_completion(self):
        """Completion of paths."""
        self.vimiv.commandline.entry.set_text(":./vimiv/testimages/ar")
        self.vimiv.completions.complete()
        expected_completions = ["arch-logo.png", "arch_001.jpg"]
        self.assertEqual(self.vimiv.completions.completions,
                         expected_completions)

    def test_tabbing(self):
        """Tabbing through completions."""
        # Complete to last matching character
        self.vimiv.commandline.entry.set_text(":cl")
        self.vimiv.completions.complete()
        expected_text = ":clear_t"
        received_text = self.vimiv.commandline.entry.get_text()
        self.assertEqual(expected_text, received_text)
        # First result
        self.vimiv.completions.complete()
        expected_text = ":clear_thumbs"
        received_text = self.vimiv.commandline.entry.get_text()
        self.assertEqual(expected_text, received_text)
        # Second result
        self.vimiv.completions.complete()
        expected_text = ":clear_trash"
        received_text = self.vimiv.commandline.entry.get_text()
        self.assertEqual(expected_text, received_text)
        # First again
        self.vimiv.completions.complete(inverse=True)
        expected_text = ":clear_thumbs"
        received_text = self.vimiv.commandline.entry.get_text()
        self.assertEqual(expected_text, received_text)


if __name__ == '__main__':
    main()
