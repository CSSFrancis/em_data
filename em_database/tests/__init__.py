import pytest

from em_database import get_data_dir, set_data_dir, reset_data_dir

def test_download_directory():
    reset_data_dir()
    print(get_data_dir())
