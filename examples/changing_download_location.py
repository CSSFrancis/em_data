"""
Changing the Download Location
==============================

This example demonstrates how to change the default download location for datasets
in the `em_database` package. By default, datasets are downloaded to a predefined
directory, but users can customize this location as needed.
"""

from em_database import get_data_dir, set_data_dir, reset_data_dir



# Display the current download directory
print("Current download directory:", get_data_dir())
# Set a new download directory
new_directory = "/path/to/your/custom/directory"  # Replace with your desired path
set_data_dir(new_directory)
print("Updated download directory:", get_data_dir())
# Reset to the default download directory
reset_data_dir()
print("Reset download directory:", get_data_dir())




