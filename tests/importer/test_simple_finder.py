from dataclasses import dataclass
from unittest import TestCase

from custom_imports.importer import SimpleFinder


class TestSimpleFinder(TestCase):
    def test_simple_finder(self):
        @dataclass
        class SimpleLocator:
            fullname: str

        finder = SimpleFinder(
            locate_module=lambda fullname, path, target: SimpleLocator(fullname)
        )

        self.assertEqual(
            SimpleLocator("fake_module"), finder.find_module_locator("fake_module", [])
        )
