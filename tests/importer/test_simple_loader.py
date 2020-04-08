import sys
from dataclasses import dataclass
from unittest import TestCase

from custom_imports.importer import Module, ModuleSpec, SimpleLoader

PY_36 = sys.version_info[:2] == (3, 6)


class TestSimpleLoader(TestCase):
    def test_simple_loader(self):
        @dataclass
        class SimpleModule:
            value: str = ""

            def set_value(self, value):
                self.value = value

        loader = SimpleLoader(
            module_type=SimpleModule,
            module_type_kwargs={"value": "Initial value"},
            load_module=SimpleModule.set_value,
        )

        module_spec = ModuleSpec(
            "fake_module", None, loader_state="Lorem ipsum, dolor sit amet"
        )

        with self.subTest("Create module"):
            module = loader.create_module(module_spec)

            self.assertIsInstance(module, SimpleModule)
            self.assertEqual("Initial value", module.value)

            if PY_36:
                self.assertTrue(issubclass(type(module), Module))
            else:
                self.assertIsInstance(module, Module)

        with self.subTest("Load module"):
            module.__spec__ = module_spec
            loader.exec_module(module)

            self.assertIsInstance(module, SimpleModule)
            self.assertEqual("Lorem ipsum, dolor sit amet", module.value)

            if PY_36:
                self.assertTrue(issubclass(type(module), Module))
            else:
                self.assertIsInstance(module, Module)
