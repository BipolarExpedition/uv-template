# Reminder to self

## Preferred libraries

### CLI

`typer` and `rich`. verbose, debug, version in a common callback. Special "experiment" command for dev time experiments

Consider `textual` if rich is not enough


### database

`sqlmodel`. Uses pydantic style structures and will work with sqlite or mariadb
`sqlite3` for simple and direct sqlite


### GUI

PySide6


### http calls

`requests`, or `httpx` if async. 

`requests_cached.CachedSession('cache_name', backend='sqlite', expire_After=86400)` for http request caching


### testing

Consider using `hypothesize` for random testing data


### file formats

- toml :: standard `tomllib` for readonly, `tomli_w` for read write.
- ini  :: standard `configparser`, `config = configparser.ConfigParser()` `config.read('filename.ini')` `config.get('section', 'key')`, `config['section'] = { 'key' :'value' }`, `config['section']['key'] = 'value'`


### System folders

- `from platformdirs import user_cache_path` `cache_path = user_cache_path("identifier")`
- or `os.environ.get("XDG_CACHE_HOME)` if linux

### Speeding up slower functions on repeat calls

- Disk caching     :: `from diskcache import Cache`, `cache_obj = Cache(filename)`, `@cache_obj(expire=60*60, tag="optional")`
- Memory caching   :: `@functools.lru_cache(maxsize=num_entries)`
- Property caching :: `@functools.cached_property`

### unique data structures

- text :: `Lark`. Define the grammar. Define a class for transforming the pieces into python types.
- data :: `kaitaistruct`


### web application

`fastapi`


### Portable binaries
- pyoxidizer or pyinstaller


### misc notes

- `pydantic.SecretStr` is useful for preventing log bleeding
- `contextlib.suppress` to just ignore an exception
- From the standard library, `import atexit`, `atexit.register(funcNoParams)`, `atexit.register(funcWithParams, 'val1', var2='val2')`, `atexit.unregister(funcWithOrWithoutParams)`. Can use decorator `@atexit.register` for functions without parameters.
- >=3.10 now has match-case as pythonic case selector
- `typing.TypedDict` makes type hinting a dict easy, but is normal dict at runtime. Also consider `pydantic`
- remember `type` is available for >= 3.12
- for `pathlib.Path`: walk, glob, rglob, relative_to, read_text, write_text, open, touch, unlink

