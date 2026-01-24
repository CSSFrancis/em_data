import yaml
from pathlib import Path
from collections import defaultdict


def parse_datasets(yaml_dir):
    """Parse all YAML files and organize by technique."""
    datasets_by_technique = defaultdict(list)

    for yaml_file in Path(yaml_dir).glob("*.yaml"):
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)

        for name, info in data.items():
            technique = info.get('technique', 'Unknown')
            datasets_by_technique[technique].append({
                'name': name,
                'description': info.get('description', ''),
                'tags': info.get('tags', []),
                'source': info.get('source', ''),
                'file': info.get('file', ''),
                'license': info.get('license', ''),
                'detector': info.get('detector', 'Unknown'),
                'detector_manufacturer': info.get('detector_manufacturer', 'Unknown')
            })

    return dict(datasets_by_technique)


def generate_html_table(datasets_by_technique):
    """Generate HTML with filterable table and technique tabs."""
    all_tags = set()
    all_detectors = {}  # Changed to dict: {manufacturer: [detectors]}
    technique_tags = {}
    technique_detectors = {}

    for technique, datasets in datasets_by_technique.items():
        tags = set()
        detectors = {}
        for dataset in datasets:
            tags.update(dataset['tags'])
            all_tags.update(dataset['tags'])
            manufacturer = dataset.get('detector_manufacturer', 'Unknown')
            detector = dataset.get('detector', 'Unknown')

            if manufacturer not in detectors:
                detectors[manufacturer] = set()
            detectors[manufacturer].add(detector)

            if manufacturer not in all_detectors:
                all_detectors[manufacturer] = set()
            all_detectors[manufacturer].add(detector)

        technique_tags[technique] = sorted(tags)
        technique_detectors[technique] = {m: sorted(d) for m, d in detectors.items()}

    all_detectors = {m: sorted(d) for m, d in all_detectors.items()}

    technique_tags_json = __import__('json').dumps(technique_tags)
    technique_detectors_json = __import__('json').dumps(technique_detectors)
    all_tags_sorted = sorted(all_tags)
    all_detectors_json = __import__('json').dumps(all_detectors)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; position: relative; }}
            .tabs {{ margin: 10px 0; }}
            .tab-button {{ padding: 8px 12px; margin-right: 6px; cursor: pointer; border: 1px solid #ccc; background: #f9f9f9; }}
            .tab-button.active {{ background: #e9e9e9; font-weight: bold; }}
            .filter-dropdown {{ position: relative; display: inline-block; }}
            .filter-button {{ cursor: pointer; padding: 4px 8px; background: #fff; border: 1px solid #ccc; border-radius: 3px; margin-left: 8px; }}
            .filter-content {{ display: none; position: absolute; background: white; border: 1px solid #ccc; padding: 10px; z-index: 1000; min-width: 250px; max-height: 300px; overflow-y: auto; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }}
            .filter-dropdown.active .filter-content {{ display: block; }}
            .filter-checkbox {{ display: block; margin: 5px 0; }}
            .manufacturer-group {{ margin: 10px 0; padding-left: 10px; }}
            .manufacturer-label {{ font-weight: bold; margin: 8px 0 4px 0; }}
            .detector-checkbox {{ display: block; margin: 3px 0; padding-left: 20px; }}
            th:nth-child(5), td:nth-child(5) {{ min-width: 200px; }}
        </style>
    </head>
    <body>
        <h1>EM Datasets</h1>

        <div class="tabs" id="techTabs">
            <!-- Tabs will be injected here -->
        </div>

        <table id="datasetsTable">
            <thead>
                <tr>
                    <th>Technique</th>
                    <th>Dataset</th>
                    <th>Description</th>
                    <th>
                        Tags
                        <div class="filter-dropdown" id="tagsFilter">
                            <span class="filter-button">▼</span>
                            <div class="filter-content" id="tagsContent"></div>
                        </div>
                    </th>
                    <th>
                        Detector
                        <div class="filter-dropdown" id="detectorFilter">
                            <span class="filter-button">▼</span>
                            <div class="filter-content" id="detectorContent"></div>
                        </div>
                    </th>
                    <th>File</th>
                    <th>License</th>
                </tr>
            </thead>
            <tbody>
    """

    for technique in sorted(datasets_by_technique.keys()):
        for dataset in datasets_by_technique[technique]:
            tags_str = ', '.join(dataset['tags'])
            manufacturer = dataset.get('detector_manufacturer', 'Unknown')
            detector = dataset.get('detector', 'Unknown')
            detector_full = f"{manufacturer} - {detector}"
            html += f"""            <tr data-tags="{tags_str}" data-technique="{technique}" data-detector="{detector}" data-manufacturer="{manufacturer}">
                <td>{technique}</td>
                <td><strong>{dataset['name']}</strong></td>
                <td>{dataset['description']}</td>
                <td>{tags_str}</td>
                <td>{detector_full}</td>
                <td><a href="{dataset['source']}">{dataset['file']}</a></td>
                <td>{dataset['license']}</td>
            </tr>
    """

    html += f"""        </tbody>
        </table>
        <script>
            const techniqueTags = {technique_tags_json};
            const techniqueDetectors = {technique_detectors_json};
            const allTags = {__import__('json').dumps(all_tags_sorted)};
            const allDetectors = {all_detectors_json};
            let currentTechnique = 'All';

            function createTabs() {{
                const tabs = document.getElementById('techTabs');
                const allButton = document.createElement('button');
                allButton.textContent = 'All';
                allButton.className = 'tab-button active';
                allButton.onclick = () => filterTechnique('All');
                tabs.appendChild(allButton);

                Object.keys(techniqueTags).sort().forEach(tech => {{
                    const btn = document.createElement('button');
                    btn.textContent = tech;
                    btn.className = 'tab-button';
                    btn.onclick = () => filterTechnique(tech);
                    tabs.appendChild(btn);
                }});
            }}

            function renderFilterCheckboxes(containerId, items) {{
                const container = document.getElementById(containerId);
                container.innerHTML = '';
                items.forEach(item => {{
                    const label = document.createElement('label');
                    label.className = 'filter-checkbox';
                    const input = document.createElement('input');
                    input.type = 'checkbox';
                    input.value = item;
                    input.onchange = filterTable;
                    label.appendChild(input);
                    label.appendChild(document.createTextNode(' ' + item));
                    container.appendChild(label);
                }});
            }}

            function renderDetectorCheckboxes(detectors) {{
                const container = document.getElementById('detectorContent');
                container.innerHTML = '';

                Object.keys(detectors).sort().forEach(manufacturer => {{
                    const group = document.createElement('div');
                    group.className = 'manufacturer-group';

                    const mfrLabel = document.createElement('label');
                    mfrLabel.className = 'manufacturer-label filter-checkbox';
                    const mfrInput = document.createElement('input');
                    mfrInput.type = 'checkbox';
                    mfrInput.value = manufacturer;
                    mfrInput.dataset.type = 'manufacturer';
                    mfrInput.onchange = (e) => {{
                        const detectorInputs = group.querySelectorAll('input[data-manufacturer="' + manufacturer + '"]');
                        detectorInputs.forEach(input => input.checked = e.target.checked);
                        filterTable();
                    }};
                    mfrLabel.appendChild(mfrInput);
                    mfrLabel.appendChild(document.createTextNode(' ' + manufacturer));
                    group.appendChild(mfrLabel);

                    detectors[manufacturer].forEach(detector => {{
                        const label = document.createElement('label');
                        label.className = 'detector-checkbox';
                        const input = document.createElement('input');
                        input.type = 'checkbox';
                        input.value = detector;
                        input.dataset.manufacturer = manufacturer;
                        input.onchange = filterTable;
                        label.appendChild(input);
                        label.appendChild(document.createTextNode(' ' + detector));
                        group.appendChild(label);
                    }});

                    container.appendChild(group);
                }});
            }}

            function updateFilters(technique) {{
                const tags = technique === 'All' ? allTags : (techniqueTags[technique] || []);
                const detectors = technique === 'All' ? allDetectors : (techniqueDetectors[technique] || {{}});
                renderFilterCheckboxes('tagsContent', tags);
                renderDetectorCheckboxes(detectors);
            }}

            function setActiveTab(name) {{
                const buttons = document.querySelectorAll('.tab-button');
                buttons.forEach(b => {{
                    b.classList.toggle('active', b.textContent === name);
                }});
            }}

            function filterTechnique(technique) {{
                currentTechnique = technique;
                setActiveTab(technique);
                updateFilters(technique);
                filterTable();
            }}

            function filterTable() {{
                const selectedTags = Array.from(document.querySelectorAll('#tagsContent input:checked')).map(cb => cb.value);
                const selectedDetectors = Array.from(document.querySelectorAll('#detectorContent input:checked:not([data-type="manufacturer"])')).map(cb => cb.value);
                const rows = document.querySelectorAll('#datasetsTable tbody tr');

                rows.forEach(row => {{
                    const rowTechnique = row.dataset.technique;
                    if (currentTechnique !== 'All' && rowTechnique !== currentTechnique) {{
                        row.style.display = 'none';
                        return;
                    }}

                    const rowTags = row.dataset.tags ? row.dataset.tags.split(', ').filter(t => t) : [];
                    const rowDetector = row.dataset.detector;

                    const tagsMatch = selectedTags.length === 0 || selectedTags.every(tag => rowTags.includes(tag));
                    const detectorMatch = selectedDetectors.length === 0 || selectedDetectors.includes(rowDetector);

                    row.style.display = (tagsMatch && detectorMatch) ? '' : 'none';
                }});
            }}

            // Toggle dropdown visibility
            document.querySelectorAll('.filter-dropdown .filter-button').forEach(btn => {{
                btn.onclick = (e) => {{
                    e.stopPropagation();
                    const dropdown = btn.parentElement;
                    document.querySelectorAll('.filter-dropdown').forEach(d => {{
                        if (d !== dropdown) d.classList.remove('active');
                    }});
                    dropdown.classList.toggle('active');
                }};
            }});

            // Close dropdowns when clicking outside
            document.addEventListener('click', () => {{
                document.querySelectorAll('.filter-dropdown').forEach(d => d.classList.remove('active'));
            }});

            // Prevent dropdown from closing when clicking inside
            document.querySelectorAll('.filter-content').forEach(content => {{
                content.onclick = (e) => e.stopPropagation();
            }});

            // Initialize UI
            createTabs();
            updateFilters('All');
        </script>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":

    # Usage
    datasets = parse_datasets('datasets')
    print(datasets)
    html_output = generate_html_table(datasets)

    output_path = Path('docs/datasets.html')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open('w', encoding='utf-8') as f:
        f.write(html_output)