# custom_imports

Tools to hook into Python's `import` syntax.

These hooks can allow you to `import` config files,
modules written in different languages,
or even create entirely virtual modules.

## Basic Usage

Included in `custom_imports` are some sample importers,
`json_importer`, `cfg_importer`, `ini_importer`, and `CSVImporter`.

When registered, these importers allow you to `import` the corresponding file
types as though they were Python modules.

For example,

`server_config.ini`

```ini
[environment]
server_name = prod
debug = no

[database]
host = https://example.com
port = 27017
username = <username>
password = <password>
```

`connections.py`

```python
import server_config

if server_config.environment.debug:
    setup_logging()

db_client = DatabaseClient(**server_config.database)
```

## Registration

Importers can be registered with `importer.register()`.

```python
from custom_imports import ini_importer

ini_importer.register()

import server_config
```

Alternatively, you can use the importer as a context manager:

```python
with ini_importer:
    import server_config
```

and the importer deregisters itself once the `with` block has been terminated.

## Deregistration

Import hooks modify `sys.meta_path`, which is global, so it's a bad idea to
leave your importers hanging around if you intend for your code to be used as
part of a larger project.

For example, if two modules use different flavors of CSV, then one of them is
going to be unable to import their CSV files.

Thankfully, once a module has been imported for the first time, it is stored in
the module cache, and so you no longer need the importer.

To keep your `sys.meta_path` clear, you can deregister an importer once you're
finished with it.
This can be done either with `importer.deregister()`, or by using the importer
as a context manager.

## Environment-wide Setup

On the other hand, it can be ugly needing to have a non-`import` (the importer
registration) before an `import` (your custom module type).

If you *are* the only project needing to use this Python environment, then you
can register an importer environment-wide.
To do so, create a `custom-imports.pth` file in your environment's
`site-packages` folder with the following contents:

```pth
import custom_imports; custom_imports.ini_importer.register()
```

For multiple importers, repeat the entire line, replacing the importer used.

If your project uses an importer in this way, be sure to include this step in
your project's environment setup instructions.

## Reference

### `Finder`

Module `Finder`s search for a module among the various paths available.
If it finds a module, it returns a "locator" for that module,
which can be any non-`None` Python object that contains all the
information required to immediately locate the module.
If it fails to find a module, it returns `None`.

Module `Finder`s do not attempt to construct the module,
they only find their locators.

Custom `Finder`s should inherit from `Finder` and override the `find_module_locator` method.

Two module `Finder`s are provided by default:

#### `SimpleFinder`

A basic Finder class.

```python
SimpleFinder(
    locate_module=func,
)
```

Finds a module locator by calling `func(fullname, path, target)`.

#### `FileModuleExtensionFinder`

Finder for file based modules by file extensions.

A file based module is a module that is generated from a single file.

```python
FileModuleExtensionFinder(ext)
```

This Finder interprets a module's name as a filename, with extension `ext`.
Parent modules are interpreted as directories.

This provides a relative path, which is searched for on the standard module
search path. If a file with that relative path is found, then the absolute
`Path` of that file is returned as its module locator.

### `Loader`

Module `Loader`s take module locators, and construct the module at that location.

Custom `Loader`s should inherit from `Loader` and override the `create_module` and `exec_module` methods.

Two module `Loader`s are provided by default:

#### `SimpleLoader`

A basic Loader class.

```python
SimpleLoader(
    module_type=cls,
    module_type_kwargs=kwargs,
    load_module=func,
)
```

Creates an empty module by calling the equivalent of `cls(**kwargs)`,
and executes it by calling `func(module, module_locator)`.

#### `FileModuleLoader`

Loader for file based modules.

A file based module is a module that is generated from a single file.

```python
FileModuleLoader(
    module_type=cls,
    module_type_kwargs=kwargs,
    read_module=func,
)
```

This Loader takes a `Path` to the file to be loaded as its module locator,
creates an empty module by calling the equivalent of `cls(**kwargs)`,
and executes it by calling `func(module, file)`.

The file handle passed to `func` is closed after `func` terminates.

### `Importer`

A basic Importer class.

```python
Importer(
    finder=finder,
    loader=loader,
)
```

When registered, this `Importer` overloads `import` syntax to additionally
attempt to use `finder` to find modules, and `loader` to load them.

Register an `Importer` with `importer.register()`.
Deregister an `Importer` with `importer.deregister()`.

May also be used as a context manager:

```python
with foo_importer:
    import foo
```

with the importer registering itself at the start of the block, and
deregistering itself at the end.

### Sample importers

#### `json_importer`

When registered, imports `.json` files as `dict`s.

#### `cfg_importer`

When registered, import `.cfg` files using `ConfigParser`,
with attribute notation.

#### `ini_importer`

When registered, import `.ini` files using `ConfigParser`,
with attribute notation.

#### `CSVImporter`

When instantiated and registered, import `.csv` files using the provided CSV reader.

```python
CSVImporter(
    csv_reader=csv_reader,
    csv_reader_kwargs=kwargs,
)
```

This importer loads a module using the result of `csv_reader(file, **kwargs)`.

`csv_reader` should be a CSV reader class (for example, `csv.reader`, or
`csv.DictReader`).
