import sys
from dataclasses import dataclass
from unittest import TestCase

from custom_imports.importer import Importer, SimpleFinder, SimpleLoader


@dataclass
class SimpleLocator:
    fullname: str


@dataclass
class SimpleModule:
    value: str = ""

    def set_value(self, locator):
        self.value = locator.fullname


class TestImporter(TestCase):
    def setUp(self):
        finder = SimpleFinder(
            locate_module=lambda fullname, path, target: SimpleLocator(fullname)
        )

        loader = SimpleLoader(
            module_type=SimpleModule, load_module=SimpleModule.set_value
        )

        self.importer = Importer(finder=finder, loader=loader)

    def test_importer(self):
        importer = self.importer

        with self.subTest("Module unavailable before registration"), self.assertRaises(
            ImportError
        ):
            import fake_module

        with self.subTest("Module importable"):
            importer.register()
            import fake_module

            self.assertIsInstance(fake_module, SimpleModule)
            self.assertEqual("fake_module", fake_module.value)

        with self.subTest("Module unavailable after deregistration"):
            del sys.modules["fake_module"]
            importer.deregister()

            with self.assertRaises(ImportError):
                import fake_module

    def test_importer_context_manager(self):
        with self.subTest("Module available inside context manager"):
            with self.importer:
                import fake_module

            self.assertIsInstance(fake_module, SimpleModule)
            self.assertEqual("fake_module", fake_module.value)

        with self.subTest("Module unavailable outside context manager"):
            del sys.modules["fake_module"]

            with self.assertRaises(ImportError):
                import fake_module
