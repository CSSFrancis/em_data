import sys
import re
import yaml
from pathlib import Path

def parse_issue_body(text):
    # Simple regex-based parser for the fields
    fields = {
        "Dataset Name": r"--Dataset Name--\s*(.*)",
        "Author": r"--Author--\s*(.*)",
        "URL": r"--URL--\s*(.*)",
        "Checksum": r"--Checksum--\s*(.*)",
        "Description": r"--Description--\s*([\s\S]*?)--Detector Manufacturer--",
        "Detector Manufacturer": r"--Detector Manufacturer--\s*(.*)",
        "Detector Model": r"Detector Model\s*(.*)",
        "Microscope Vendor": r"Microscope Vendor\s*(.*)",
        "Microscope Model": r"Microscope Model\s*(.*)",
        "Accelerating Voltage": r"Accelerating Voltage\s*(.*)",
        "Dataset License": r"Dataset License\s*(.*)",
        "Technique": r"Technique\s*(.*)",
        "Tags": r"Tags\s*(.*)"
    }
    data = {}
    for key, pattern in fields.items():
        m = re.search(pattern, text)
        if m:
            data[key] = m.group(1).strip()
        else:
            data[key] = ""
    return data

def build_yaml(data):
    # Convert tags to list
    tags = [t.strip() for t in data["Tags"].split(",") if t.strip()]
    # Use author as dataset name (sanitize)
    d_name = re.sub(r'\W+', '', data["Dataset Name"])
    yaml_data = {
        d_name: {
            "description": data["Description"],
            "source": data["URL"],
            "detector_manufacturer": data["Detector Manufacturer"],
            "detector": data["Detector Model"],
            "microscope_vendor": data["Microscope Vendor"],
            "microscope": data["Microscope Model"],
            "voltage": data["Accelerating Voltage"],
            "license": data["Dataset License"],
            "technique": data["Technique"],
            "tags": tags,
            "authors": {
                data["Author"]: {}
            }
        }
    }
    return yaml_data, dataset_name

if __name__ == "__main__":
    issue_file = sys.argv[1]
    out_dir = Path(sys.argv[2])
    with open(issue_file) as f:
        text = f.read()
    data = parse_issue_body(text)
    yaml_data, dataset_name = build_yaml(data)
    out_path = out_dir / f"{dataset_name}.yaml"
    with open(out_path, "w") as f:
        f.write("# $schema: ../json-schema.json\n")
        yaml.dump(yaml_data, f, sort_keys=False)