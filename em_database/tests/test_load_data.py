"""Tests for downloading datasets.

The expensive part of testing a download index is not the download - it is
knowing that every ``source`` still resolves. Checking that costs a HEAD request
per dataset, so it is done for all of them. Actually pulling bytes only proves
that pooch and the checksum verification are wired up correctly, which is
identical for every entry, so it is done once with the smallest file in the
index. The large downloads are marked ``slow`` and deselected by default; run
them with ``pytest -m slow``.
"""

import urllib.error
import urllib.request

import pytest

import em_database.data as data
from em_database.data import MgONanoCrystals, NiEBSDLarge

try:
    from quantem.core.io.file_readers import read_4dstem

    QUANTEM_AVAILABLE = True
except ImportError:
    QUANTEM_AVAILABLE = False

# The smallest file in the index (34 kB). Used wherever a test needs a real
# download to exercise pooch rather than to exercise a particular dataset.
TINY_DATASET = "CuZnHAADF"

ALL_DATASETS = sorted(data.__all__)


def _head(url, timeout=60):
    """Return the response for a HEAD request, following redirects."""
    request = urllib.request.Request(
        url, method="HEAD", headers={"User-Agent": "em_database tests"}
    )
    return urllib.request.urlopen(request, timeout=timeout)


@pytest.mark.parametrize("name", ALL_DATASETS)
def test_source_url_resolves(name):
    """Every dataset's source URL must still exist.

    This is what actually breaks over time - a Zenodo record superseded, a
    GitHub ref rewritten - and it is invisible until someone tries to download.
    """
    dataset = getattr(data, name)()
    url = f"{dataset.source}/{dataset.file}"
    try:
        response = _head(url)
    except urllib.error.HTTPError as error:
        pytest.fail(f"{name}: {url} returned HTTP {error.code}")
    except urllib.error.URLError as error:  # pragma: no cover - transient
        pytest.skip(f"{name}: network unavailable ({error.reason})")
    assert response.status == 200, f"{name}: {url} returned {response.status}"


@pytest.mark.parametrize("name", ALL_DATASETS)
def test_metadata_is_complete(name):
    """Entries need enough metadata for pooch to fetch and verify them."""
    dataset = getattr(data, name)()
    assert dataset.source, f"{name} has no source"
    assert dataset.file, f"{name} has no file"
    assert dataset.description, f"{name} has no description"
    assert dataset.checksum and dataset.checksum.startswith("md5:"), (
        f"{name} has no md5 checksum, so a corrupt or truncated download "
        f"would go unnoticed"
    )


def test_download_verifies_checksum(tmp_path):
    """A real download, to prove pooch and checksum verification are wired up."""
    dataset = getattr(data, TINY_DATASET)()
    path = dataset.download(destination=tmp_path, progressbar=False)
    assert (tmp_path / dataset.file).exists()
    assert path == str(tmp_path / dataset.file)


def test_download_is_cached(tmp_path):
    """A second download of the same file must not refetch it."""
    dataset = getattr(data, TINY_DATASET)()
    first = dataset.download(destination=tmp_path, progressbar=False)
    mtime = (tmp_path / dataset.file).stat().st_mtime_ns
    second = dataset.download(destination=tmp_path, progressbar=False)
    assert first == second
    assert (tmp_path / dataset.file).stat().st_mtime_ns == mtime


def test_download_rejects_a_bad_checksum(tmp_path):
    """A wrong checksum must raise rather than hand back the file."""
    dataset = getattr(data, TINY_DATASET)()
    dataset.checksum = "md5:" + "0" * 32
    with pytest.raises(Exception):
        dataset.download(destination=tmp_path, progressbar=False)


@pytest.mark.slow
def test_download_ni_ebsd(tmp_path):
    dataset = NiEBSDLarge()
    dataset.download(destination=tmp_path, progressbar=False)
    assert (tmp_path / "patterns_v2.h5").exists()


@pytest.mark.slow
def test_download_mgo_nanocrystals(tmp_path):
    dataset = MgONanoCrystals()
    dataset.download(destination=tmp_path, progressbar=False)
    assert (tmp_path / dataset.file).exists()


@pytest.mark.slow
@pytest.mark.skipif(not QUANTEM_AVAILABLE, reason="quantem is not installed")
def test_quantem_loading(tmp_path):
    dataset = MgONanoCrystals()
    file_path = dataset.download(destination=tmp_path, progressbar=False)
    read_4dstem(file_path)
