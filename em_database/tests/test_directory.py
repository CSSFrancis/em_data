"""Tests for the data directory handling.

These exercise where files land, not what is in them, so they use the smallest
dataset in the index rather than a large one.
"""

import os

import pytest

import em_database
from em_database import data
from em_database.tests.test_load_data import TINY_DATASET

DEFAULT_DIR = os.path.join(os.path.expanduser("~"), "em_database")


@pytest.fixture(autouse=True)
def _restore_data_dir():
    """Never leave a stray data dir set for the next test."""
    yield
    em_database.reset_data_dir()


def test_get_data_dir():
    assert em_database.get_data_dir() == DEFAULT_DIR


def test_set_data_dir(tmp_path):
    em_database.set_data_dir(str(tmp_path))
    assert em_database.get_data_dir() == str(tmp_path)


def test_reset_data_dir(tmp_path):
    em_database.set_data_dir(str(tmp_path))
    em_database.reset_data_dir()
    assert em_database.get_data_dir() == DEFAULT_DIR


def test_saving_to_configured_dir(tmp_path):
    """A dataset downloads into whatever data dir is configured."""
    em_database.set_data_dir(str(tmp_path))
    dataset = getattr(data, TINY_DATASET)()
    dest = dataset.download(progressbar=False)
    assert os.path.exists(os.path.join(str(tmp_path), dataset.file))
    # a second download must reuse the file rather than refetch it
    assert dataset.download(progressbar=False) == dest


def test_saving_to_explicit_dir(tmp_path):
    """An explicit destination overrides the configured data dir."""
    other = tmp_path / "elsewhere"
    em_database.set_data_dir(str(tmp_path / "configured"))
    dataset = getattr(data, TINY_DATASET)()
    dest = dataset.download(destination=str(other), progressbar=False)
    assert "elsewhere" in dest
    assert (other / dataset.file).exists()


def test_filepath_reports_missing_and_present(tmp_path):
    """filepath() is None until the file is there, then returns the path."""
    em_database.set_data_dir(str(tmp_path))
    dataset = getattr(data, TINY_DATASET)()
    assert dataset.filepath() is None
    dataset.download(progressbar=False)
    assert dataset.filepath() == os.path.join(str(tmp_path), dataset.file)
