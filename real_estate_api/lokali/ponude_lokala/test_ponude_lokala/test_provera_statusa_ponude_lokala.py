from real_estate_api.lokali.lokali_api.models import Lokali
from real_estate_api.lokali.ponude_lokala.models import PonudeLokala


class TestPromenaStatusLokalaIzPonudeLokala:
    """Testitanje statusa Lokala ukoliko dodje do promene-brisanja u Ponudama Lokala"""

    def test_da_li_su_tri_ponuda_lokala_kreirane(self, nove_tri_ponude_lokala_fixture):
        """ Da li su tri Ponude Lokala kreirane u bazi. """

        broj_ponuda_lokala_from_db = PonudeLokala.objects.all().count()
        assert broj_ponuda_lokala_from_db == 3

    def test_da_li_je_lokal_inicijalizovan(self, nove_tri_ponude_lokala_fixture):
        """ Da li je inicijalizovan Lokal. """

        ponuda_lokala = PonudeLokala.objects.all().first()
        lokal = Lokali.objects.filter(id_lokala__exact=ponuda_lokala.lokali.id_lokala)

        assert lokal.all().count() == 1

    def test_izmeni_ponudu_lokala_potencijalna_status_lokala_dostupan(self,
                                                                      client,
                                                                      nova_jedna_ponuda_lokala_fixture,
                                                                      ):
        ponuda_lokala = PonudeLokala.objects.all().first()
        lokal = Lokali.objects.filter(id_lokala__exact=ponuda_lokala.lokali.id_lokala).first()

        # Proveri inicijalan status Lokala (Treba da je: "DOSTUPAN")
        assert lokal.status_prodaje_lokala == Lokali.StatusProdajeLokala.DOSTUPAN

        # Set status Ponude Lokala na POTENCIJALAN
        ponuda_lokala.status_ponude_lokala = PonudeLokala.StatusPonudeLokala.POTENCIJALAN
        ponuda_lokala.save()

        # Now, chaeck id status Ponude Lokala is  set to POTENCIJALAN
        assert ponuda_lokala.status_ponude_lokala == PonudeLokala.StatusPonudeLokala.POTENCIJALAN

        # Provera odobrenja Ponude Lokala.
        assert ponuda_lokala.odobrenje is False

        # Now, get again Ponude Lokala.
        izmenjen_lokal = Lokali.objects.all().first()
        assert izmenjen_lokal.status_prodaje_lokala == Lokali.StatusProdajeLokala.DOSTUPAN

    def test_izmeni_ponudu_lokala_rezervisan_status_lokala_rezervisan(self,
                                                                      client,
                                                                      nova_jedna_ponuda_lokala_fixture,
                                                                      ):
        ponuda_lokala = PonudeLokala.objects.all().first()
        lokal = Lokali.objects.filter(id_lokala__exact=ponuda_lokala.lokali.id_lokala).first()

        # Proveri inicijalan status Lokala (Treba da je: "DOSTUPAN")
        assert lokal.status_prodaje_lokala == Lokali.StatusProdajeLokala.DOSTUPAN

        # Set status Ponude Lokala na DOSTUPAN
        ponuda_lokala.status_ponude_lokala = PonudeLokala.StatusPonudeLokala.REZERVISAN
        ponuda_lokala.save()

        # Now, chaeck id status Ponude Lokala is  set to REZERVISAN
        assert ponuda_lokala.status_ponude_lokala == PonudeLokala.StatusPonudeLokala.REZERVISAN

        # Provera odobrenja Ponude Lokala.
        assert ponuda_lokala.odobrenje is True

        # Now, get again Ponude Lokala.
        izmenjen_lokal = Lokali.objects.all().first()
        assert izmenjen_lokal.status_prodaje_lokala == Lokali.StatusProdajeLokala.REZERVISAN

    def test_izmeni_ponudu_lokala_kupljen_status_lokala_prodat(self,
                                                               client,
                                                               nova_jedna_ponuda_lokala_fixture,
                                                               ):
        ponuda_lokala = PonudeLokala.objects.all().first()
        lokal = Lokali.objects.filter(id_lokala__exact=ponuda_lokala.lokali.id_lokala).first()

        # Proveri inicijalan status Lokala (Treba da je: "DOSTUPAN")
        assert lokal.status_prodaje_lokala == Lokali.StatusProdajeLokala.DOSTUPAN

        # Set status Ponude Lokala na KUPLJEN
        ponuda_lokala.status_ponude_lokala = PonudeLokala.StatusPonudeLokala.KUPLJEN
        ponuda_lokala.save()

        # Now, chaeck id status Ponude Lokala is  set to KUPLJEN
        assert ponuda_lokala.status_ponude_lokala == PonudeLokala.StatusPonudeLokala.KUPLJEN

        # Provera odobrenja Ponude Lokala.
        assert ponuda_lokala.odobrenje is True

        # Now, get again Ponude Lokala.
        izmenjen_lokal = Lokali.objects.all().first()
        assert izmenjen_lokal.status_prodaje_lokala == Lokali.StatusProdajeLokala.PRODAT

    def test_kreiraj_ponudu_lokala_potencijalan_status_stana_rezervisan(self,
                                                                        client,
                                                                        nova_jedna_ponuda_lokala_fixture,
                                                                        ):
        # TODO(Ivana): Implementirati situaciju kada se obrise POTENCIJALNA Ponuda Lokala:
        # TODO(Ivana): PONUDA -> POTENCIJALNA  ||  LOKAL -> REZERVISAN
        ponuda_lokala = PonudeLokala.objects.all().first()
        lokal = Lokali.objects.filter(id_lokala__exact=ponuda_lokala.lokali.id_lokala).first()

        # TODO(Ivana): 1. Kreirati Ponudu Lokala koja je rezervisana da bi status Lokala bio "REZERVISAN".
        # TODO(Ivana): 2. Kreirati Ponudu Lokala status "POTENCIJALAN", i proveriti da li je Lokal ostao REZERVISAN.
        # TODO(Ivana): 3. Takodje proveriti "ODOBRENJE PONUDE".

    def test_obrisi_ponudu_lokala_potencijalan_status_lokala_prodat(self,
                                                                    client,
                                                                    nova_jedna_ponuda_lokala_fixture,
                                                                    ):
        # TODO(Ivana): 1. Kreirati Ponudu Lokala koja je u statusu: "KUPLJEN" da bi status Lokala bio "KUPLJEN".
        # TODO(Ivana): 2. Obrisati Ponudu Lokala status "POTENCIJALAN", i proveriti da li je Lokal ostao "KUPLJEN".
        assert True

    def test_obrisi_ponudu_lokala_potencijalan_status_lokala_rezervisan(self,
                                                                        client,
                                                                        nova_jedna_ponuda_lokala_fixture,
                                                                        ):
        # TODO(Ivana): 1. Kreirati Ponudu Lokala koja je u statusu: "REZERVISAN" da bi status Lokala bio "REZERVISAN".
        # TODO(Ivana): 2. Obrisati Ponudu Lokala status "POTENCIJALAN", i proveriti da li je Lokal ostao "REZERVISAN".
        assert True

    def test_obrisi_ponudu_lokala_kupljen_status_lokala_rezervisan(self,
                                                                   client,
                                                                   nova_jedna_ponuda_lokala_fixture,
                                                                   ):
        # TODO(Ivana): 1. Kreirati Ponudu Lokala koja je u statusu: "KUPLJEN" da bi status Lokala bio "KUPLJEN".
        # TODO(Ivana): 1. Kreirati Ponudu Lokala koja je u statusu: "REZERVISAN" da bi status Lokala bio "KUPLJEN".
        # TODO(Ivana): 2. Obrisati Ponudu Lokala status "KUPLJEN", i proveriti da li je Lokal ostao "REZERVISAN".
        assert True

    def test_obrisi_sve_ponude_lokala_status_lokala_dostupan(self,
                                                             client,
                                                             nova_jedna_ponuda_lokala_fixture,
                                                             ):
        # TODO(Ivana): 1. Obrisati sve Ponude Lokala i Proveriti status Lokala (Treba da je dostupan)
        assert True
