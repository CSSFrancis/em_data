"""Auto-generated dataset classes from YAML Files for downloading data."""

from pathlib import Path

import yaml

from em_database._create_stubs import build_docstring
from em_database.downloadable_dataset import DownloadableDataset

__all__ = []
datasets_path = Path(__file__).parent.parent / "datasets"
for dataset_path in sorted(datasets_path.rglob("*.y*ml")):
    data_dict_yaml = yaml.safe_load(dataset_path.read_text(encoding="utf-8"))
    for name in data_dict_yaml:
        class_name = name.replace(" ", "_").replace("-", "_")
        data_dict = data_dict_yaml[name]
        _new_class = type(
            class_name,
            (DownloadableDataset,),
            {"_spec": data_dict, "__doc__": build_docstring(data_dict)},
        )
        globals()[class_name] = _new_class
        __all__.append(class_name)
