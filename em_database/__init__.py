### Example datasets ###
from em_database import data
from em_database.config import settings
from em_database.downloadable_dataset import DownloadableDataset
from em_database.query import filter, list_datasets, search  # noqa: A004

__all__ = []


def get_data_dir():
    """
    Get the directory where example datasets are stored.

    Returns
    -------
    str
        Path to the example datasets directory.
    """
    from em_database import config

    return config.data_dir()


def set_data_dir(path: str, persist: bool = True):
    """
    Set the directory where example datasets are stored.

    Parameters
    ----------
    path : str
        Path to the desired example datasets directory.
    persist : bool, optional
        If True (the default), remember the choice across sessions by writing it
        to the settings file. Pass False for a one-off, in-memory change.
    """
    settings["data_dir"] = str(path)
    if persist:
        settings.save()


def reset_data_dir():
    """
    Reset the example datasets directory to the default location, clearing any
    saved choice.
    """
    settings.reset("data_dir")


def get_setting(key: str, default=None):
    """Read a value from :data:`em_database.settings`."""
    return settings.get(key, default)


def set_setting(key: str, value, persist: bool = True):
    """Set a value in :data:`em_database.settings`, persisting it by default."""
    settings[key] = value
    if persist:
        settings.save()


def browse(**kwargs):
    """
    Open the interactive dataset browser in Jupyter.

    Returns an `anywidget` widget listing every dataset grouped by technique,
    showing which are downloaded, revealing full metadata on hover, and
    downloading on click with a live progress toast. Requires the optional
    `anywidget` dependency (`pip install em-database[widget]`).

    ``display(em_database)`` renders the same browser.
    """
    from em_database.widget import browse as _browse

    return _browse(**kwargs)


__all__ = [
    "list_datasets",
    "search",
    "filter",
    "get_data_dir",
    "set_data_dir",
    "reset_data_dir",
    "get_setting",
    "set_setting",
    "settings",
    "browse",
    "data",
    "DownloadableDataset",
]


# Let ``display(em_database)`` render the browser. Reassigning the module's
# __class__ to a ModuleType subclass is a supported pattern (see PEP 562) and is
# what lets the package itself carry a rich Jupyter repr.
import sys as _sys  # noqa: E402
from types import ModuleType as _ModuleType  # noqa: E402


class _EmDatabaseModule(_ModuleType):
    def _repr_mimebundle_(self, include=None, exclude=None, **kwargs):
        try:
            widget = browse()
        except Exception:
            return {
                "text/plain": (
                    "em_database — install the interactive browser with "
                    "`pip install em-database[widget]`, then call "
                    "em_database.browse()."
                )
            }
        return widget._repr_mimebundle_(**kwargs)


_sys.modules[__name__].__class__ = _EmDatabaseModule
