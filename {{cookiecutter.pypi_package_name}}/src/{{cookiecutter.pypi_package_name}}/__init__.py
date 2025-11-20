import importlib.metadata

# Refer to pyproject.toml or package metadata for metadata


def _get_version(meta_name: str | None) -> str:
    try:
        if meta_name:
            return importlib.metadata.version(meta_name)
    except importlib.metadata.PackageNotFoundError:
        pass
    except Exception:
        return "0.0.0-error"

    return "0.0.0-dev"


def _get_license_type(metadata: importlib.metadata.PackageMetadata) -> str:
    """Return SPDX short identifier or Unknown"""
    try:
        _license = metadata["License-Expression"]
        # Special case for my preferred license
        if not _license:
            _license = metadata["License"]
            if _license and _license.lower().startswith("mit license"):
                return "MIT"
        else:
            return _license
    except Exception:
        pass

    return "Unknown"


def _get_project_name(metadata: importlib.metadata.PackageMetadata) -> str:
    """Return project name"""
    return metadata.get("Name") or __package__ or __name__ or "Unknown Project"


# Define failsafe values
PROJECT_AUTHOR = "{{ cookiecutter.full_name }}"
PROJECT_COPYRIGHT = "Copyright (c) {{ cookiecutter.full_name }}"
PROJECT_EMAIL = "{{ cookiecutter.email }}"
PROJECT_LICENSE = "Unknown"
PROJECT_NAME = "# {{ cookiecutter.project_name }}"
PROJECT_VERSION = "0.0.0-error"

# Try to set values, but avoid failing

attempts = [
    __package__,
    __name__,
    __package__.replace("_", "-") if __package__ else None,
    __package__.replace("-", "_") if __package__ else None,
]

_mdata: importlib.metadata.PackageMetadata | None = None
_meta_name = None
for chosen_name in attempts:
    try:
        if chosen_name:
            _meta_name = chosen_name
            _mdata = importlib.metadata.metadata(_meta_name)
            break
    except importlib.metadata.PackageNotFoundError:
        continue
    except Exception:
        pass

__version__ = _get_version(_meta_name)
PROJECT_VERSION = __version__

if _mdata:
    try:
        PROJECT_NAME = _get_project_name(_mdata)
    except Exception:
        PROJECT_NAME = "Unknown"

    try:
        PROJECT_LICENSE = _get_license_type(_mdata)
    except Exception:
        PROJECT_LICENSE = "Unknown"

    if "Author" in _mdata:
        __author__ = _mdata["Author"]
        PROJECT_AUTHOR = __author__
    else:
        PROJECT_AUTHOR = "Unknown"

    if "Author-Email" in _mdata:
        __email__ = _mdata["Author-Email"]
        try:
            if "<" in __email__:
                # Split at the first "<"
                _split = __email__.split("<", 1)
                # Don't capture after ">", as there may be multiple emails
                PROJECT_EMAIL = _split[-1].split(">", 1)[0]
                __email__ = PROJECT_EMAIL

                if PROJECT_AUTHOR == "Unknown" and len(_split[0].strip()) > 0:
                    PROJECT_AUTHOR = _split[0].strip()
                    __author__ = PROJECT_AUTHOR
            else:
                PROJECT_EMAIL = __email__

        except Exception:
            pass
    else:
        PROJECT_EMAIL = ""

    try:
        PROJECT_COPYRIGHT = f"Copyright (c) {PROJECT_AUTHOR} ({PROJECT_EMAIL})\nLicense: {PROJECT_LICENSE}"
    except Exception:
        PROJECT_COPYRIGHT = "Copyright (c) Unknown"

try:
    del _get_license_type
    del _get_project_name
    del _get_version
    globals().pop("_mdata", None)
    globals().pop("_meta_name", None)
    globals().pop("_split", None)
except Exception:
    pass
