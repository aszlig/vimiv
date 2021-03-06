#!/usr/bin/env python
# encoding: utf-8
"""Test fileactions.py for vimiv's test suite."""

import os
import shutil
from unittest import TestCase, main
import vimiv.fileactions as fileactions
import vimiv.main as v_main
from vimiv.parser import parse_config


class FileActionsTest(TestCase):
    """Fileactions Tests."""

    def setUp(self):
        self.working_directory = os.getcwd()
        os.chdir("vimiv")

    def test_move_to_trash(self):
        """Move file to trash."""
        os.chdir("testimages/")
        shutil.copyfile("arch_001.jpg", "image_to_edit.jpg")
        filename = os.path.abspath("image_to_edit.jpg")
        files = [filename]
        fileactions.move_to_trash(files)
        trashed_file = os.path.expanduser("~/.vimiv/Trash/image_to_edit.jpg")
        self.assertTrue(os.path.isfile(trashed_file))
        # Repeat, to check if backing up works
        shutil.copyfile("arch_001.jpg", "image_to_edit.jpg")
        fileactions.move_to_trash(files)
        trashed_file1 = os.path.expanduser("~/.vimiv/Trash/image_to_edit.jpg.1")
        self.assertTrue(os.path.isfile(trashed_file1))
        shutil.copyfile("arch_001.jpg", "image_to_edit.jpg")
        fileactions.move_to_trash(files)
        trashed_file2 = os.path.expanduser("~/.vimiv/Trash/image_to_edit.jpg.2")
        self.assertTrue(os.path.isfile(trashed_file2))
        # Clear the files
        os.remove(trashed_file)
        os.remove(trashed_file1)

    def test_is_image(self):
        """Check whether file is an image."""
        os.chdir("testimages/")
        self.assertTrue(fileactions.is_image("arch_001.jpg"))
        self.assertFalse(fileactions.is_image("not_an_image.jpg"))

    def test_clear(self):
        """Clear Trash/Thumbnails."""
        settings = parse_config()
        vimiv = v_main.Vimiv(settings, [], 0)
        vimiv.main()
        thumbdir = os.path.expanduser("~/.vimiv/Thumbnails")
        trashdir = os.path.expanduser("~/.vimiv/Trash")
        if not os.path.isdir("Thumbnail_bak"):
            shutil.copytree(thumbdir, "Thumbnail_bak")
        if not os.path.isdir("Trash_bak"):
            shutil.copytree(trashdir, "Trash_bak")
        # Make sure there are some files in the directories
        os.system("touch ~/.vimiv/Trash/foo")
        os.system("touch ~/.vimiv/Thumbnails/foo")
        vimiv.fileextras.clear("Thumbnails")
        vimiv.fileextras.clear("Trash")
        self.assertEqual(os.listdir(thumbdir), [])
        self.assertEqual(os.listdir(trashdir), [])
        # Move backups back to directory
        shutil.rmtree(thumbdir)
        shutil.rmtree(trashdir)
        shutil.move("Thumbnail_bak", thumbdir)
        shutil.move("Trash_bak", trashdir)

    def test_format_files(self):
        """Format files according to a formatstring."""
        shutil.copytree("testimages/", "testimages_to_format/")
        os.chdir("testimages_to_format")
        settings = parse_config()
        paths, index = fileactions.populate(["arch_001.jpg"])
        vimiv = v_main.Vimiv(settings, paths, index)
        vimiv.main()
        vimiv.fileextras.format_files("formatted_")
        files = [fil for fil in os.listdir() if "formatted_" in fil]
        files = sorted(files)
        expected_files = ["formatted_001.jpg", "formatted_002",
                          "formatted_003.bmp", "formatted_004.svg",
                          "formatted_005.tiff", "formatted_006.png"]
        self.assertEqual(files, expected_files)
        os.chdir("..")
        shutil.rmtree("testimages_to_format")
        # Should not work without a path
        vimiv.paths = []
        vimiv.fileextras.format_files("formatted_")
        err_message = vimiv.statusbar.left_label.get_text()
        expected_message = "No files in path"
        self.assertEqual(expected_message, err_message)
        # Should not work in library
        vimiv.library.focus(True)
        vimiv.fileextras.format_files("formatted_")
        err_message = vimiv.statusbar.left_label.get_text()
        expected_message = "Format only works on opened image files"
        self.assertEqual(expected_message, err_message)

    def test_format_files_with_exif(self):
        """Format files according to a formatstring with EXIF data."""
        shutil.copytree("testimages/", "testimages_to_format/")
        os.chdir("testimages_to_format")
        settings = parse_config()
        paths, index = fileactions.populate(["arch_001.jpg"])
        vimiv = v_main.Vimiv(settings, paths, index)
        vimiv.main()
        vimiv.fileextras.format_files("formatted_")
        files = [fil for fil in os.listdir() if "formatted_" in fil]
        files = sorted(files)
        expected_files = ["formatted_001.jpg", "formatted_002",
                          "formatted_003.bmp", "formatted_004.svg",
                          "formatted_005.tiff", "formatted_006.png"]
        self.assertEqual(files, expected_files)
        # These files have no exif info
        vimiv.fileextras.format_files("formatted_%y_")
        err_message = vimiv.statusbar.left_label.get_text()
        expected_message = "No exif data for %s available" % \
            (os.path.abspath("formatted_001.jpg"))
        self.assertEqual(expected_message, err_message)
        # Should not work without a path
        vimiv.paths = []
        vimiv.fileextras.format_files("formatted_foo_")
        err_message = vimiv.statusbar.left_label.get_text()
        expected_message = "No files in path"
        self.assertEqual(expected_message, err_message)
        # Should not work in library
        vimiv.library.focus(True)
        vimiv.fileextras.format_files("formatted_bar_")
        err_message = vimiv.statusbar.left_label.get_text()
        expected_message = "Format only works on opened image files"
        self.assertEqual(expected_message, err_message)
        # Make sure nothing changed
        files = [fil for fil in os.listdir() if "formatted_" in fil]
        files = sorted(files)
        self.assertEqual(files, expected_files)
        # Clean up
        os.chdir("..")
        shutil.rmtree("testimages_to_format")
        # TODO file with exif data

    def tearDown(self):
        os.chdir(self.working_directory)


if __name__ == '__main__':
    main()
