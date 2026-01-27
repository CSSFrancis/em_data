from em_database import NiEBSDLarge, MgONanoCrystals


def test_download_ni_ebsd():
    dataset = NiEBSDLarge()
    dataset.download()

def test_download_custom_location(tmp_path):
    dataset = NiEBSDLarge()
    dataset.download(destination=tmp_path)
    assert (tmp_path / "patterns_v2.h5").exists()
