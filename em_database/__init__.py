### Example datasets ###
from idlelib.window import registry

import pooch
import os
import yaml
from em_database.downloadable_dataset import DownloadableDataset
from em_database._create_stubs import build_docstring
__all__ = []


if "EM_DATABASE_DATA_DIR" not in os.environ:
    # set the default dir to User's home directory + "/emdata"
    print("Setting default EM_DATABASE_DATA_DIR")
    os.environ["EM_DATABASE_DATA_DIR"] = os.path.join(
        os.path.expanduser("~") + "\em_database"
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

# Map all the datasets in the "datasets" folder
# recursively travel down
for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), "datasets")):
    for file in files:
        if file.endswith(".yaml") or file.endswith(".yml"):
            dataset_path = os.path.join(root, file)
            with open(dataset_path, 'r') as f:
                data_dict_yaml = yaml.safe_load(f)
                for name in data_dict_yaml:
                    class_name = name.replace(' ', '_').replace('-', '_')
                    data_dict = data_dict_yaml[name]
                    print(data_dict)


                    def make_init(data):
                        def __init__(self):
                            super(self.__class__, self).__init__(**data)

                        return __init__


                    new_class = type(class_name,
                                     (DownloadableDataset,),
                                     {"__init__": make_init(data_dict),
                                      "__doc__": build_docstring(data_dict)})

                    # Add to module globals and __all__
                    globals()[class_name] = new_class
                    __all__.append(class_name)
