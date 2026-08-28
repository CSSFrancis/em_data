"""A browsable catalogue of the datasets, grouped by technique.

This is the data model behind :func:`em_database.browse`: it turns the
``em_database.data`` classes into rows a UI can draw - grouped by technique,
marked downloaded or not, each carrying the metadata a user hovers to read. It
downloads nothing and opens no files, so it is cheap enough to rebuild on every
render (the one thing that changes underfoot is which files are on disk, which
is a single ``Path.exists`` per dataset).
"""

from __future__ import annotations

import inspect
from pathlib import Path

from em_database.downloadable_dataset import DownloadableDataset

# Techniques in the order the browser should show them - the modalities the
# collection is built around first, then anything else alphabetically.
TECHNIQUE_ORDER = ("4D-STEM", "EELS", "EDS", "EBSD", "STEM", "In-situ TEM", "Cryo-EM")


def datasets() -> list[tuple[str, DownloadableDataset]]:
    """``(name, dataset)`` for every dataset ``em_database.data`` exposes.

    Filtered by ``issubclass`` so the base class and incidental imports in the
    module namespace stay out; sorted by name for a stable order.
    """
    import em_database.data as data

    out: list[tuple[str, DownloadableDataset]] = []
    for name in getattr(data, "__all__", None) or dir(data):
        if name.startswith("_"):
            continue
        obj = getattr(data, name, None)
        if (
            not inspect.isclass(obj)
            or obj is DownloadableDataset
            or not issubclass(obj, DownloadableDataset)
        ):
            continue
        try:
            out.append((name, obj()))
        except Exception:
            continue
    return sorted(out, key=lambda kv: kv[0].lower())


def resolve(name: str) -> DownloadableDataset | None:
    """The dataset instance for a catalogue name, or ``None``."""
    import em_database.data as data

    obj = getattr(data, str(name), None)
    if not inspect.isclass(obj) or not issubclass(obj, DownloadableDataset):
        return None
    return obj()


def _technique(ds) -> str:
    md = getattr(ds, "metadata", None) or {}
    return str(md.get("technique") or "Other").strip() or "Other"


def _join(*parts) -> str:
    return " ".join(str(p).strip() for p in parts if p and str(p).strip())


def _declared_shape(ds) -> str | None:
    """The shape em-database declares in the dataset's YAML, if it does.

    Only declared shapes are used - reading it out of a downloaded file would
    mean opening the file (and depending on a reader), which the catalogue
    deliberately never does.
    """
    md = getattr(ds, "metadata", None) or {}
    for source in (md, ds):
        for attr in ("shape", "data_shape"):
            val = source.get(attr) if isinstance(source, dict) else getattr(source, attr, None)
            if val:
                return val.strip() if isinstance(val, str) else "×".join(str(v) for v in val)
    return None


def _authors(md) -> tuple[list[str], list[str]]:
    """``(names, affiliations)`` from the dataset's ``authors`` metadata.

    Authors are usually ``{name: {affiliation: ...}}``; also tolerate a plain
    list of names.
    """
    authors = md.get("authors")
    if isinstance(authors, dict):
        names = list(authors.keys())
        affiliations = []
        for value in authors.values():
            if isinstance(value, dict) and value.get("affiliation"):
                affiliations.append(str(value["affiliation"]))
        return names, affiliations
    return [str(a) for a in (authors or [])], []


def _location(path: Path | None) -> str | None:
    """Which data directory a downloaded file came from: "shared" or "user"."""
    if path is None:
        return None
    from em_database import config

    parent = path.resolve().parent
    shared = {d.resolve() for d in config.shared_data_dirs()}
    return "shared" if parent in shared else "user"


def entry(name: str, ds: DownloadableDataset) -> dict:
    """One catalogue row - everything the browser draws for a dataset."""
    md = getattr(ds, "metadata", None) or {}
    try:
        path = ds.filepath()
    except Exception:
        path = None
    names, affiliations = _authors(md)
    row = {
        "name": name,
        "technique": _technique(ds),
        "size": str(getattr(ds, "data_size", "") or ""),
        "shape": _declared_shape(ds),
        "downloaded": path is not None,
        "location": _location(path),
        "path": str(path) if path else "",
        "description": str(getattr(ds, "description", "") or ""),
        "detector": _join(getattr(ds, "detector_manufacturer", ""), getattr(ds, "detector", "")),
        "microscope": _join(md.get("microscope_vendor"), md.get("microscope_model")),
        "voltage": str(md.get("voltage") or ""),
        "tags": [str(t) for t in (md.get("tags") or [])],
        "authors": names,
        "license": str(getattr(ds, "license", "") or ""),
        "doi": str(getattr(ds, "doi", "") or ""),
        "source": str(getattr(ds, "source", "") or ""),
        "file": str(getattr(ds, "file", "") or ""),
    }
    # One lowercased blob the search box matches against, so a query like
    # "Carter Francis" (an author) or "Direct Electron" (an affiliation) finds
    # every dataset it touches - not just the name.
    searchable = [
        name,
        row["technique"],
        row["description"],
        row["detector"],
        row["microscope"],
        row["voltage"],
        row["license"],
        row["doi"],
        row["file"],
        row["shape"] or "",
        " ".join(row["tags"]),
        " ".join(names),
        " ".join(affiliations),
    ]
    row["search"] = " ".join(str(s) for s in searchable if s).lower()
    return row


def _order(technique: str):
    try:
        return (0, TECHNIQUE_ORDER.index(technique))
    except ValueError:
        return (1, technique.lower())


def catalogue() -> dict:
    """The whole browser payload, grouped by technique.

    ``{"data_dir", "groups": [{"technique", "items"}], "n_downloaded",
    "n_total"}`` - one group per technique in :data:`TECHNIQUE_ORDER`, then any
    others alphabetically.
    """
    import em_database

    items = [entry(name, ds) for name, ds in datasets()]
    by_tech: dict[str, list[dict]] = {}
    for it in items:
        by_tech.setdefault(it["technique"], []).append(it)
    groups = [{"technique": t, "items": by_tech[t]} for t in sorted(by_tech, key=_order)]
    return {
        "data_dir": str(em_database.get_data_dir()),
        "groups": groups,
        "n_downloaded": sum(1 for it in items if it["downloaded"]),
        "n_total": len(items),
    }
