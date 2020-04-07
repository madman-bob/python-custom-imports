import csv
from configparser import ConfigParser
from importlib import import_module
from types import ModuleType
from unittest import TestCase

from more_properties import cached_class_property

from custom_imports.sample_importers import CSVImporter, ini_importer, json_importer


class TestSampleImporterMixin:
    importer = None
    name = None
    expected_type = None
    expected_value = None

    @cached_class_property
    def full_name(cls):
        return f"tests.sample_files.{cls.name}"

    @classmethod
    def setUpClass(cls):
        cls.importer.register()

    def tearDown(self):
        import sys

        if self.full_name in sys.modules:
            del sys.modules[self.full_name]

    @classmethod
    def tearDownClass(cls):
        cls.importer.deregister()

    def test_sample_importer(self):
        module = import_module(self.full_name)

        self.assertIsInstance(module, ModuleType)
        self.assertIsInstance(module, self.expected_type)
        self.assertEqual(self.expected_value, module)


class TestJsonImporter(TestSampleImporterMixin, TestCase):
    importer = json_importer
    name = "john_smith"
    expected_type = dict
    expected_value = {
        "firstName": "John",
        "lastName": "Smith",
        "isAlive": True,
        "age": 27,
        "address": {
            "streetAddress": "21 2nd Street",
            "city": "New York",
            "state": "NY",
            "postalCode": "10021-3100",
        },
        "phoneNumbers": [
            {"type": "home", "number": "212 555-1234"},
            {"type": "office", "number": "646 555-4567"},
        ],
        "children": [],
        "spouse": None,
    }


class TestIniImporter(TestSampleImporterMixin, TestCase):
    importer = ini_importer
    name = "db_config"
    expected_type = ConfigParser
    expected_value = {
        "owner": {"full_name": "John Doe", "organization": "Acme Widgets Inc."},
        "database": {
            "server": "192.0.2.62",
            "port": 143,
            "file": "payroll.dat",
            "debug": False,
        },
    }

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        ConfigParser.__eq__ = lambda self, other: self._sections == other

    def test_attribute_notation(self):
        from tests.sample_files import db_config

        self.assertEqual("John Doe", db_config.owner.full_name)
        self.assertEqual(143, db_config.database.port)
        self.assertEqual(False, db_config.database.debug)


class TestCSVImporter(TestSampleImporterMixin, TestCase):
    importer = CSVImporter(
        csv_reader=csv.DictReader, csv_reader_kwargs={"quoting": csv.QUOTE_NONNUMERIC},
    )
    name = "cars"
    expected_type = list
    expected_value = [
        {
            "Year": 1997,
            "Make": "Ford",
            "Model": "E350",
            "Description": "ac, abs, moon",
            "Price": 3000.00,
        },
        {
            "Year": 1999,
            "Make": "Chevy",
            "Model": 'Venture "Extended Edition"',
            "Description": "",
            "Price": 4900.00,
        },
        {
            "Year": 1999,
            "Make": "Chevy",
            "Model": 'Venture "Extended Edition, Very Large"',
            "Description": "",
            "Price": 5000.00,
        },
        {
            "Year": 1996,
            "Make": "Jeep",
            "Model": "Grand Cherokee",
            "Description": "MUST SELL!\nair, moon roof, loaded",
            "Price": 4799.00,
        },
    ]
