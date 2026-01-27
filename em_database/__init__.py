### Example datasets ###
from idlelib.window import registry

import pooch
import os
import yaml
from em_database.downloadable_dataset import DownloadableDataset
from em_database._create_stubs import build_docstring
from em_database import data
__all__ = []


if "EM_DATABASE_DATA_DIR" not in os.environ:
    # set the default dir to User's home directory + "/emdata"
    print("Setting default EM_DATABASE_DATA_DIR")
    os.environ["EM_DATABASE_DATA_DIR"] = os.path.join(
        os.path.expanduser("~") + "\\em_database"
    )



def get_data_dir():
    """
    Get the directory where example datasets are stored.

    Returns
    -------
    str
        Path to the example datasets directory.
    """
    return  os.environ["EM_DATABASE_DATA_DIR"]

def set_data_dir(path: str):
    """
    Set the directory where example datasets are stored.

    Parameters
    ----------
    path : str
        Path to the desired example datasets directory.
    """
    os.environ["EM_DATABASE_DATA_DIR"] = path

def reset_data_dir():
    """
    Reset the example datasets directory to the default location.
    """
    os.environ["EM_DATABASE_DATA_DIR"] = os.path.join(
        os.path.expanduser("~") + "\em_database"
    )


__all__ =  ['get_data_dir', 'set_data_dir', 'reset_data_dir',"data"]