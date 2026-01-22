from em_database import NiEBSDLarge, MgONanoCrystals




def test_download_mgo_nanocrystals():
    dataset = NiEBSDLarge()

    dataset.download()