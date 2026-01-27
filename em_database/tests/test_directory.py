import em_database
import pytest
import os
from em_database import data
def test_get_data_dir():
    default_dir = em_database.get_data_dir()
    assert default_dir==  os.path.join(os.path.expanduser("~") + "\em_database")

def test_set_data_dir():
    test_dir = os.path.join(os.path.expanduser("~"), "test_em_database_dir")
    em_database.set_data_dir(test_dir)
    assert em_database.get_data_dir() == test_dir
    # Clean up by resetting to default
    em_database.reset_data_dir()
    default_dir = em_database.get_data_dir()
    assert default_dir==  os.path.join(os.path.expanduser("~") + "\em_database")

def test_saving_to_default_dir():
    dataset = data.NiEBSDLarge()
    dataset.download()
    assert os.path.exists(os.path.join(em_database.get_data_dir(), "patterns_v2.h5"))
    ## make sure that it doesn't download the second time.
    dest = dataset.download()
    assert dest == os.path.join(em_database.get_data_dir(), "patterns_v2.h5")

def test_saving_to_non_default_dir():
    test_dir = os.path.join(os.path.expanduser("~"), "test_em_database_dir")
    em_database.set_data_dir(test_dir)
    dataset = em_database.data.NiEBSDLarge()
    dataset.download()
    assert os.path.exists(os.path.join(em_database.get_data_dir(), "patterns_v2.h5"))
    ## make sure that it doesn't download the second time.
    dest = dataset.download()
    assert dest == os.path.join(em_database.get_data_dir(), "patterns_v2.h5")
    assert "test_em_database_dir" in dest
    # Clean up by resetting to default
    em_database.reset_data_dir()
    default_dir = em_database.get_data_dir()
    assert default_dir==  os.path.join(os.path.expanduser("~") + "\em_database")


def test_reset_data_dir():
    test_dir = os.path.join(os.path.expanduser("~"), "test_em_database_dir")
    em_database.set_data_dir(test_dir)
    em_database.reset_data_dir()
    default_dir = em_database.get_data_dir()
    assert default_dir==  os.path.join(os.path.expanduser("~") + "\em_database")