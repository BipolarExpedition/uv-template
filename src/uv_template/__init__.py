import importlib.metadata

# Refer to pyproject.toml or package metadata for metadata


def get_version() -> str:
    try:
        return importlib.metadata.version(__package__ or __name__)
    except importlib.metadata.PackageNotFoundError:
        return "0.0.0-dev"
    except Exception:
        return "0.0.0-error"


def get_license_type(metadata: importlib.metadata.PackageMetadata) -> str:
    """Return SPDX short identifier or Unknown"""
    try:
        _license = metadata["License-Expression"]
        # Special case for my prefered license
        if not _license:
            _license = metadata["License"]
            if _license and _license.lower().startswith("mit license"):
                return "MIT"
        else:
            return _license
    except Exception:
        pass

    return "Unknown"


def get_project_name(metadata: importlib.metadata.PackageMetadata) -> str:
    """Return project name"""
    return metadata.get("Name") or __package__ or __name__ or "Unknown Project"


# Define failsafe values
PROJECT_AUTHOR = "Unknown"
PROJECT_COPYRIGHT = "Copyright (c) Unknown"
PROJECT_EMAIL = ""
PROJECT_LICENSE = "Unknown"
PROJECT_NAME = "Unknown"
PROJECT_VERSION = "0.0.0-error"

# Try to set values, but avoid failing
try:
    mdata: importlib.metadata.PackageMetadata = importlib.metadata.metadata(__package__ or __name__)

    __version__ = get_version()
    PROJECT_VERSION = __version__

    if not mdata:
        raise ValueError("Failed to get package metadata")

    PROJECT_NAME = get_project_name(mdata)
    PROJECT_LICENSE = get_license_type(mdata)

    if "Author" in mdata:
        __author__ = mdata["Author"]
        PROJECT_AUTHOR = __author__
    else:
        PROJECT_AUTHOR = "Unknown"

    if "Author-Email" in mdata:
        __email__ = mdata["Author-Email"]
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
except Exception:
    pass

try:
    del get_license_type
    del get_project_name
    del get_version
    globals().pop("mdata", None)
    globals().pop("_split", None)
except Exception:
    pass
