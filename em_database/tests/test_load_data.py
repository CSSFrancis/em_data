from em_database import NiEBSDLarge, MgONanoCrystals





def test_download_ni_ebsd():
    dataset = NiEBSDLarge()
    dataset.download()