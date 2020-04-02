from dataclasses import dataclass
from pathlib import Path
from unittest import TestCase

from custom_imports.file_module import FileModuleLoader
from custom_imports.importer import Module, ModuleSpec

project_root = Path(__file__).parents[2]


class TestFileModuleLoader(TestCase):
    def test_file_module_loader(self):
        @dataclass
        class SimpleModule:
            value: str = ""

            def set_value(self, file):
                self.value = file.read()

        loader = FileModuleLoader(
            module_type=SimpleModule,
            module_type_kwargs={"value": "Initial value"},
            read_module=SimpleModule.set_value,
        )

        module_spec = ModuleSpec(
            "fake_module",
            None,
            loader_state=project_root / "tests/sample_files/lipsum.txt",
        )

        with self.subTest("Create module"):
            module = loader.create_module(module_spec)

            self.assertIsInstance(module, SimpleModule)
            self.assertEqual("Initial value", module.value)

            self.assertIsInstance(module, Module)

        with self.subTest("Load module"):
            module.__spec__ = module_spec
            loader.exec_module(module)

            self.assertIsInstance(module, SimpleModule)
            self.assertEqual("Lorem ipsum\n", module.value)

            self.assertIsInstance(module, Module)
