""" Auto-generated dataset classes from YAML Files for downloading data."""
import os
import yaml
from em_database.downloadable_dataset import DownloadableDataset
from em_database._create_stubs import build_docstring

# Map all the datasets in the "datasets" folder
# recursively travel down
__all__ = []
for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), "../datasets")):
    for file in files:
        if file.endswith(".yaml") or file.endswith(".yml"):
            dataset_path = os.path.join(root, file)
            with open(dataset_path, 'r') as f:
                data_dict_yaml = yaml.safe_load(f)
                for name in data_dict_yaml:
                    class_name = name.replace(' ', '_').replace('-', '_')
                    data_dict = data_dict_yaml[name]
                    def _make_init(data):
                        def __init__(self):
                            super(self.__class__, self).__init__(**data)

                        return __init__


                    _new_class = type(class_name,
                                     (DownloadableDataset,),
                                     {"__init__": _make_init(data_dict),
                                      "__doc__": build_docstring(data_dict)})

                    # Add to module globals and __all__
                    globals()[class_name] = _new_class
                    __all__.append(class_name)