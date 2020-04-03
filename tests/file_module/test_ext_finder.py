from pathlib import Path
from unittest import TestCase

from custom_imports.file_module import FileModuleExtensionFinder

project_root = Path(__file__).parents[2]


class TestFileModuleExtensionFinder(TestCase):
    def test_file_extension_module_finder_find_path(self):
        finder = FileModuleExtensionFinder("txt")

        with self.subTest("Find file path"):
            self.assertEqual(
                project_root / "tests/sample_files/lipsum.txt",
                finder.find_path("tests.sample_files.lipsum", [project_root]),
            )

        with self.subTest("Fail to find non-existent path"):
            self.assertEqual(
                None, finder.find_path("tests.sample_files.foo", [project_root])
            )

        with self.subTest("Fail to find without search path"):
            self.assertEqual(None, finder.find_path("tests.sample_files.lipsum", []))

    def test_file_extension_module_finder_find_module_locator(self):
        finder = FileModuleExtensionFinder("txt")

        self.assertEqual(
            project_root / "tests/sample_files/lipsum.txt",
            finder.find_module_locator("tests.sample_files.lipsum", []),
        )
