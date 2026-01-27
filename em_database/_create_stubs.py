import os
import yaml
from pathlib import Path
# on start up set data dir if not already set
def build_docstring(dataset_dict) -> str:
    """ Build a docstring for the dataset from its metadata. """
    doc = f""
    print(dataset_dict)
    if dataset_dict.get("description"):
        doc += f"{dataset_dict["description"]}\n\n"
    if dataset_dict.get("doi"):
        doc += f"    DOI: {dataset_dict["doi"]}\n\n"
    if dataset_dict.get("license"):
        doc += f"    License: {dataset_dict["license"]}\n\n"

    doc += "    You can download this dataset here:\n"
    doc += f"    {dataset_dict["source"]}\n\n"
    return doc

def generate_pyi_stub():
    """Generate a .pyi stub file for IDE autocomplete support."""
    stub_lines = [
        "# Auto-generated stub file for em_database",
        "from em_database.downloadable_dataset import DownloadableDataset",
        "",
    ]

    # Collect all dataset classes
    dataset_classes = []

    for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), "datasets")):
        for file in files:
            print(files)
            if file.endswith(".yaml") or file.endswith(".yml"):
                dataset_path = os.path.join(root, file)
                with open(dataset_path, 'r') as f:
                    data_dict_yaml = yaml.safe_load(f)
                    for name in data_dict_yaml:
                        data_dict = data_dict_yaml[name]
                        class_name = name.replace(' ', '_').replace('-', '_')
                        description = build_docstring(data_dict)

                        # Add class definition to stub
                        stub_lines.append(f"class {class_name}(DownloadableDataset):")
                        stub_lines.append(f'    """')
                        stub_lines.append(f"    {name}")
                        if description:
                            stub_lines.append(f"    ")
                            stub_lines.append(f"    {description}")
                        stub_lines.append(f'    """')
                        stub_lines.append("    ...")
                        stub_lines.append("")

                        dataset_classes.append(class_name)

    # Add __all__ to stub
    stub_lines.append(f"__all__ = __all__ + {dataset_classes }")

    # Write stub file
    stub_path = Path(__file__).parent / "data"/"__init__.pyi"
    with open(stub_path, 'w') as f:
        f.write('\n'.join(stub_lines))

if __name__ == "__main__":
    generate_pyi_stub()
