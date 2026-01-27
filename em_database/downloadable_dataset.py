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
                 data_size:str=None,
                 doi:str=None,
                 description:str=None,
                 detector:Optional[str]=None,
                 detector_manufacturer:Optional[str]=None,
                 **kwargs):
        self.source = source
        self.file = file
        self.checksum = checksum
        self.license = license
        self.quality = quality
        self.doi = doi
        self.data_size = data_size
        self.description = description
        self.metadata = kwargs
        self.detector_manufacturer = detector_manufacturer
        self.detector = detector

    def __repr__(self):
        return f"<{self.__class__} url={self.source}/{self.file} bytes={self.data_size}>"

    def download(self,
                 destination: str | None = None,
                 progressbar:bool = True,
                 chunk_size:int =4096) -> str:
        """ Download the dataset to the specified destination if not already present.

        By default, this will download to the defined emdata.data_dir directory. You can set
        a custom default download directory with emdata.data_dir = 'your/path/here' which will
        in turn set the corresponding environment variable.

        If the file already exists in the destination directory and the checksum matches,
        it will not be downloaded again and the existing file path will be returned.

        Parameters
        ----------
        destination : str, optional
            The directory to download the dataset to. If None, uses the default emdata.data_dir
            directory, by default None.
        progressbar : bool, optional
            Whether to show a progress bar during download, by default True.
        chunk_size : int, optional
            The chunk size to use for downloading the file, by default 4096. Increasing this value will sometimes
            increase download speed at the cost of higher memory usage.

        """

        if progressbar:
            try:
                import tqdm  # noqa: F401
            except ImportError:
                print("`tqdm` is not installed, progress bar will be disabled.")
                progressbar = False
        # Determine the destination directory
        if destination is None:
            destination = os.environ.get("EM_DATABASE_DATA_DIR",
                                         os.path.join(os.path.expanduser("~"), "em_database"))
        # Instantiate an Http downloader with a custom user agent
        headers = {"User-Agent": "em_database (https://github.com/CSSFrancis/em_data)"}
        downloader = pooch.HTTPDownloader(progressbar=progressbar,
                                          chunk_size=chunk_size,
                                          headers= headers)
        filepath = pooch.retrieve(
            url=self.source +"/"+ self.file,
            known_hash=self.checksum,
            fname=self.file,
            path=destination,
            downloader=downloader
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

