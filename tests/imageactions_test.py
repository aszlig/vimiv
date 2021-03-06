#!/usr/bin/env python
# encoding: utf-8
"""Test imageactions.py for vimiv's test suite."""

import os
import shutil
from unittest import TestCase, main
from PIL import Image
import vimiv.imageactions as imageactions


class ImageActionsTest(TestCase):
    """Imageactions Tests."""

    def setUp(self):
        self.working_directory = os.getcwd()
        os.chdir("vimiv/testimages/")
        shutil.copyfile("arch_001.jpg", "image_to_edit.jpg")
        self.filename = os.path.abspath("image_to_edit.jpg")
        self.files = [self.filename]

    def test_rotate(self):
        """Rotate image file."""
        with Image.open(self.filename) as im:
            orientation_before = im.size[0] < im.size[1]
        imageactions.rotate_file(self.files, 1)
        with Image.open(self.filename) as im:
            orientation_after = im.size[0] < im.size[1]
        self.assertNotEqual(orientation_before, orientation_after)

    def test_flip(self):
        """Flipping of files."""
        # Currently only runs through
        # TODO find a way to check if the image was flipped
        imageactions.flip_file(self.files, False)
        imageactions.flip_file(self.files, True)

    def test_thumbnails_create(self):
        """Creation of thumbnail files."""
        thumbnails = imageactions.Thumbnails(self.files, (128, 128))
        thumbnails.thumbnails_create()
        thumbnail = os.path.expanduser(
            "~/.vimiv/Thumbnails/image_to_edit.thumbnail_128x128.png")
        with Image.open(thumbnail) as im:
            thumbnail_size = max(im.size[0], im.size[1])
            self.assertEqual(thumbnail_size, 128)
        os.remove(thumbnail)

    def test_manipulate(self):
        """Manipulation of files."""
        # Currently only runs through
        # TODO find a way to check if the image was manipulated correctly
        imageactions.manipulate_all(self.filename, self.filename,
                                    [10, 10, 10, False])
        imageactions.manipulate_all(self.filename, self.filename,
                                    [0, 0, 0, True])

    def test_autorotate(self):
        """Autorotate files."""
        imageactions.autorotate(self.files)
        with Image.open(self.filename) as im:
            orientation = im.size[0] < im.size[1]
            self.assertFalse(orientation)
        imageactions.autorotate(self.files, "PIL")
        with Image.open(self.filename) as im:
            orientation = im.size[0] < im.size[1]
            self.assertFalse(orientation)

    def tearDown(self):
        os.chdir(self.working_directory)
        os.remove(self.filename)


if __name__ == '__main__':
    main()
