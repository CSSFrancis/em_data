from typing import Optional

import pooch
import os

class DownloadableDataset:

    def __init__(self,
                 source: str,
                 file: str,
                 checksum:str=None,
                 license:str=None,
                 quality:str=None,
                 doi:str=None,
                 description:str=None,
                 **kwargs):
        self.source = source
        self.file = file
        self.checksum = checksum
        self.license = license
        self.quality = quality
        self.doi = doi
        self.description = description
        self.metadata = kwargs

    def __repr__(self):
        return f"<{self.__class__} url={self.source}/{self.file} bytes={self.size()}>"

    def download(self,
                 destination: str | None = None,) -> str:
        """ Download the dataset to the specified destination if not already present.

        By default, this will download to the defined emdata.data_dir directory. You can set
        a custom default download directory with emdata.data_dir = 'your/path/here' which will
        in turn set the corresponding environment variable.

        If the file already exists in the destination directory and the checksum matches,
        it will not be downloaded again and the existing file path will be returned.
        """


        # Determine the destination directory
        if destination is None:
            destination = os.environ.get("EM_DATABASE_DATA_DIR",
                                         os.path.join(os.path.expanduser("~"), "em_database"))

        filepath = pooch.retrieve(
            url=self.source +"/"+ self.file,
            known_hash=self.checksum,
            fname=self.file,
            path=destination
        )
        return filepath

    def filepath(self) -> str:
        """ Return the local file path of the dataset if downloaded.

        If not downloaded return None. """
        destination = os.environ.get("EM_DATABASE_DATA_DIR",
                                     os.path.join(os.path.expanduser("~"), "em_database"))
        filepath = os.path.join(destination, self.file)
        if os.path.exists(filepath):
            return filepath
        else:
            return None

