"""
Settings and the Download Location
==================================

Configuration for ``em_database`` lives in a live, matplotlib-``rcParams``-style
object, ``em_database.settings``, seeded at import from a YAML file in
``~/.em_database/settings.yaml``. This example shows how to read it, change the
data directory for the session or for good, and reset it.
"""

import em_database

# %%
# The data directory is where datasets download to. It defaults to
# ``~/em_database``.
print("Current download directory:", em_database.get_data_dir())

# %%
# Change it for this session only (in memory, not written to disk).
em_database.set_data_dir("/path/to/scratch", persist=False)
print("Session directory:", em_database.get_data_dir())

# %%
# Change it and remember the choice across sessions (writes
# ``~/.em_database/settings.yaml``). ``set_data_dir`` persists by default; the
# equivalent low-level form is ``em_database.settings[...] = ...; save()``.
em_database.set_data_dir("/big/disk/em_data")            # set + persist
# em_database.settings["data_dir"] = "/big/disk/em_data"  # the same thing
# em_database.settings.save()
print("Persisted directory:", em_database.get_data_dir())

# %%
# Reset to the default location, forgetting the saved choice.
em_database.reset_data_dir()
print("Reset directory:", em_database.get_data_dir())

# %%
# Any setting can be stored, not just the data directory.
em_database.set_setting("quality", "high")
print("quality:", em_database.get_setting("quality"))

# %%
# Datasets can also be installed system-wide and shared by every user. Point
# ``EM_DATABASE_SHARED_DIR`` (or a ``shared_data_dirs`` setting, or a system
# config file) at the shared location, and ``download()`` / ``filepath()`` will
# find a pre-installed copy there before downloading into your own directory.

# %%
# Clean up so running this example leaves no settings behind.
em_database.settings.reset()
