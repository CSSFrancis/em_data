from em_database.data import NiEBSDLarge, MgONanoCrystals
try:
    from quantem.core.io.file_readers import read_4dstem
    QUANTEM_AVAILABLE = True
except ImportError:
    QUANTEM_AVAILABLE = False

def test_download_ni_ebsd():
    dataset = NiEBSDLarge()
    dataset.download()

def test_download_custom_location(tmp_path):
    dataset = NiEBSDLarge()
    dataset.download(destination=tmp_path)
    assert (tmp_path / "patterns_v2.h5").exists()


def test_download_mgo_nanocrystals():
    dataset = MgONanoCrystals()
    dataset.download()


def test_quantem_loading():
    dataset = MgONanoCrystals()
    file_path = dataset.download()
    if QUANTEM_AVAILABLE:
        data = read_4dstem(file_path)
        print(data)