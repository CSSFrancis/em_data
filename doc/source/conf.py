# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from pathlib import Path
# Import and run the build script
from em_database._build_docs import parse_datasets, generate_html_table

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'em_database'
copyright = '2026, Carter Francis'
author = 'Carter Francis'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx_gallery.gen_gallery",
    'sphinx_design',
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
master_doc = "index"
html_sidebars = {
  "datasets": []
}

def build_datasets_html(app, exception):
    """Generate datasets.html during Sphinx build"""
    if exception is not None:
        print(f"Build exception: {exception}")
    datasets_path = Path(__file__).parent.parent.parent / 'em_database' / 'datasets'
    print(f"Looking for datasets at: {datasets_path.absolute()}")
    print(f"Path exists: {datasets_path.exists()}")
    if datasets_path.exists():
        print(f"Contents: {list(datasets_path.iterdir())}")
    datasets = parse_datasets(datasets_path)
    print(f"Found {len(datasets)} datasets for documentation.")
    print(datasets)
    html_output = generate_html_table(datasets)

    output_path = Path(app.outdir) / 'datasets_db.html'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open('w', encoding='utf-8') as f:
        f.write(html_output)

def setup(app):
    app.connect('build-finished', build_datasets_html)

# sphinx_gallery
# --------------
# https://sphinx-gallery.github.io/stable/configuration.html

sphinx_gallery_conf = {
    "examples_dirs": "../../examples",
    "gallery_dirs": "examples",
    "filename_pattern": "^((?!sgskip).)*$",
    "ignore_pattern": "_sgskip.py",
    "backreferences_dir": "api",
    "doc_module": ("deapi",),
    "reference_url": {
        "deapi": None,
    },
}
