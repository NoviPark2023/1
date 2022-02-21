from real_estate_api.lokali.lokali_api.models import Lokali
from real_estate_api.lokali.ponude_lokala.models import PonudeLokala
import json
from rest_framework.reverse import reverse


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
        assert ponuda_lokala.odobrenje_kupovine_lokala is False

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
        assert ponuda_lokala.odobrenje_kupovine_lokala is True

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
        assert ponuda_lokala.odobrenje_kupovine_lokala is True

        # Now, get again Ponude Lokala.
        izmenjen_lokal = Lokali.objects.all().first()
        assert izmenjen_lokal.status_prodaje_lokala == Lokali.StatusProdajeLokala.PRODAT

    # def test_kreiraj_ponudu_lokala_potencijalan_status_lokala_rezervisan(self,
    #                                                                     client,
    #                                                                     nove_dve_ponude_lokala_fixture,
    #                                                                     ):
    #     ponuda_lokala = PonudeLokala.objects.all().last()
    #     lokal = Lokali.objects.filter(id_lokala__exact=ponuda_lokala.lokali.id_lokala).last()
    #
    #     # Status Ponude Lokala (Treba da je "REZERVISAN") i odobrenje (True)
    #     assert ponuda_lokala.status_ponude_lokala == PonudeLokala.StatusPonudeLokala.REZERVISAN
    #     assert ponuda_lokala.odobrenje_kupovine_lokala == True
    #
    #     # Status Lokala (Treba da je: "REZERVISAN")
    #     assert lokal.status_prodaje_lokala == Lokali.StatusProdajeLokala.REZERVISAN
    #
    #     # Nova Ponuda Lokala - POTENCIJALAN
    #     ponuda_lokala = PonudeLokala.objects.first()
    #     izmenjen_lokal = Lokali.objects.filter(id_lokala__exact=ponuda_lokala.lokali.id_lokala).first()
    #
    #     # Provera statusa Ponude Lokala (Treba da je: "POTENCIJALAN"),
    #     # odobrenja (False)
    #     # i statusa Prodaje Lokala (Treba da ostane: "REZERVISAN")
    #     assert ponuda_lokala.status_ponude_lokala == PonudeLokala.StatusPonudeLokala.POTENCIJALAN
    #     assert ponuda_lokala.odobrenje_kupovine_lokala == False
    #     assert izmenjen_lokal.status_prodaje_lokala == Lokali.StatusProdajeLokala.REZERVISAN

    def test_kreiraj_ponudu_lokala_potencijalan_status_lokala_rezervisan(self,
                                                                        client,
                                                                        nova_ponuda_lokala_status_rezervisan_fixture,
                                                                        ):
        """
        Kreiranje nove Ponude Lokala statusa 'POTENCIJALAN', da bi se proverilo da li ce se promeniti
        prvobitni Status Prodaje Lokala iz 'REZERVISAN' u 'DOSTUPAN', sto ne sme da se desi
        """
        id_lokala = nova_ponuda_lokala_status_rezervisan_fixture.lokali.id_lokala

        nova_ponuda_lokala_potencijalan = json.dumps(
            {
                "kupac_lokala": 1,
                "lokali": id_lokala,
                "cena_lokala_za_kupca": 54000,
                "napomena_ponude_lokala": 'string',
                "broj_ugovora_lokala": 'No55',
                "datum_ugovora_lokala": '5.2.2022',
                "status_ponude_lokala": PonudeLokala.StatusPonudeLokala.POTENCIJALAN,
                "nacin_placanja_lokala": 'Ceo iznos',
                "odobrenje_kupovine_lokala": False,
                "klijent_prodaje_lokala": 1
            }
        )

        # Prvobitna ponuda
        ponuda_lokala = PonudeLokala.objects.all().first()
        lokal = Lokali.objects.filter(id_lokala__exact=ponuda_lokala.lokali.id_lokala).first()

        # Status prvobitne Ponude Lokala (Treba da je "REZERVISAN") i odobrenje (True)
        # Status prvobitne Prodaje Lokala (Treba da je: "REZERVISAN")
        assert ponuda_lokala.status_ponude_lokala == PonudeLokala.StatusPonudeLokala.REZERVISAN
        assert ponuda_lokala.odobrenje_kupovine_lokala == True
        assert lokal.status_prodaje_lokala == Lokali.StatusProdajeLokala.REZERVISAN

        url_kreiraj_novu_ponudu_lokala = reverse('ponude-lokali:kreiraj_ponudu_lokala')

        response_kreiraj_novu_ponudu_lokala = client.post(
            url_kreiraj_novu_ponudu_lokala,
            data=nova_ponuda_lokala_potencijalan,
            content_type='application/json'
        )
        assert response_kreiraj_novu_ponudu_lokala.status_code == 201

        # Nova Ponuda Lokala - POTENCIJALAN
        nova_ponuda_lokala = PonudeLokala.objects.first()
        izmenjen_lokal = Lokali.objects.filter(id_lokala__exact=nova_ponuda_lokala.lokali.id_lokala).first()

        # Provera statusa nove Ponude Lokala (Treba da je: "POTENCIJALAN"),
        # odobrenja (False)
        # i statusa Prodaje Lokala (Treba da ostane: "REZERVISAN")
        assert nova_ponuda_lokala.status_ponude_lokala == PonudeLokala.StatusPonudeLokala.POTENCIJALAN
        assert nova_ponuda_lokala.odobrenje_kupovine_lokala == False
        assert izmenjen_lokal.status_prodaje_lokala == Lokali.StatusProdajeLokala.REZERVISAN

    def test_obrisi_ponudu_lokala_potencijalan_status_lokala_prodat(self,
                                                                    client,
                                                                    nova_ponuda_lokala_status_kupljen_fixture,
                                                                    ):
        """
        Kreiranje Ponude Lokala statusa 'KUPLJEN', da bi Status Prodaje Lokala bio PRODAT.
        Kreiranje nove Ponude Lokala statusa 'POTENCIJALAN', a zatim njeno brisanje
        da bi se proverilo da li Status Prodaje Lokala ostaje PRODAT.
        """
        id_lokala = nova_ponuda_lokala_status_kupljen_fixture.lokali.id_lokala

        nova_ponuda_lokala_potencijalan = json.dumps(
            {
                "kupac_lokala": 1,
                "lokali": id_lokala,
                "cena_lokala_za_kupca": 54000,
                "napomena_ponude_lokala": 'string',
                "broj_ugovora_lokala": 'No55',
                "datum_ugovora_lokala": '5.2.2022',
                "status_ponude_lokala": PonudeLokala.StatusPonudeLokala.POTENCIJALAN,
                "nacin_placanja_lokala": 'Ceo iznos',
                "odobrenje_kupovine_lokala": False,
                "klijent_prodaje_lokala": 1
            }
        )

        # Prvobitna ponuda
        ponuda_lokala = PonudeLokala.objects.all().first()
        lokal = Lokali.objects.filter(id_lokala__exact=ponuda_lokala.lokali.id_lokala).first()

        # Status prvobitne Ponude Lokala (Treba da je "KUPLJEN") i odobrenje (True)
        # Status prvobitne Prodaje Lokala (Treba da je: "PRODAT")
        assert ponuda_lokala.status_ponude_lokala == PonudeLokala.StatusPonudeLokala.KUPLJEN
        assert ponuda_lokala.odobrenje_kupovine_lokala == True
        assert lokal.status_prodaje_lokala == Lokali.StatusProdajeLokala.PRODAT

        url_kreiraj_novu_ponudu_lokala = reverse('ponude-lokali:kreiraj_ponudu_lokala')

        response_kreiraj_novu_ponudu_lokala = client.post(
            url_kreiraj_novu_ponudu_lokala,
            data=nova_ponuda_lokala_potencijalan,
            content_type='application/json'
        )
        assert response_kreiraj_novu_ponudu_lokala.status_code == 201

        # Nova Ponuda Lokala - POTENCIJALAN
        nova_ponuda_lokala = PonudeLokala.objects.first()
        izmenjen_lokal = Lokali.objects.filter(id_lokala__exact=nova_ponuda_lokala.lokali.id_lokala).first()

        # Provera statusa nove Ponude Lokala (Treba da je: "POTENCIJALAN"),
        # odobrenja (False)
        # i statusa Prodaje Lokala (Treba da ostane: "PRODAT")
        assert nova_ponuda_lokala.status_ponude_lokala == PonudeLokala.StatusPonudeLokala.POTENCIJALAN
        assert nova_ponuda_lokala.odobrenje_kupovine_lokala == False
        assert izmenjen_lokal.status_prodaje_lokala == Lokali.StatusProdajeLokala.PRODAT

        url_obrisi_novu_ponudu_lokala = reverse(
            'ponude-lokali:obrisi_ponudu_lokala',
            args=[nova_ponuda_lokala.id_ponude_lokala]
        )

        response = client.delete(url_obrisi_novu_ponudu_lokala)

        assert response.status_code == 204

        # Preostala prvobitna ponuda
        ponuda_lokala = PonudeLokala.objects.all().first()
        lokal = Lokali.objects.filter(id_lokala__exact=ponuda_lokala.lokali.id_lokala).first()

        # Provera Statusa Prodaje Lokala (Treba da je ostao: "PRODAT")
        assert lokal.status_prodaje_lokala == Lokali.StatusProdajeLokala.PRODAT

    def test_obrisi_ponudu_lokala_potencijalan_status_lokala_rezervisan(self,
                                                                        client,
                                                                        nova_ponuda_lokala_status_rezervisan_fixture,
                                                                        ):
        """
        Kreiranje Ponude Lokala statusa 'REZERVISAN', da bi Status Prodaje Lokala bio REZERVISAN.
        Kreiranje nove Ponude Lokala statusa 'POTENCIJALAN', a zatim njeno brisanje
        da bi se proverilo da li Status Prodaje Lokala ostaje REZERVISAN.
        """
        id_lokala = nova_ponuda_lokala_status_rezervisan_fixture.lokali.id_lokala

        nova_ponuda_lokala_potencijalan = json.dumps(
            {
                "kupac_lokala": 1,
                "lokali": id_lokala,
                "cena_lokala_za_kupca": 54000,
                "napomena_ponude_lokala": 'string',
                "broj_ugovora_lokala": 'No55',
                "datum_ugovora_lokala": '5.2.2022',
                "status_ponude_lokala": PonudeLokala.StatusPonudeLokala.POTENCIJALAN,
                "nacin_placanja_lokala": 'Ceo iznos',
                "odobrenje_kupovine_lokala": False,
                "klijent_prodaje_lokala": 1
            }
        )

        # Prvobitna ponuda
        ponuda_lokala = PonudeLokala.objects.all().first()
        lokal = Lokali.objects.filter(id_lokala__exact=ponuda_lokala.lokali.id_lokala).first()

        # Status prvobitne Ponude Lokala (Treba da je "REZERVISAN") i odobrenje (True)
        # Status prvobitne Prodaje Lokala (Treba da je: "REZERVISAN")
        assert ponuda_lokala.status_ponude_lokala == PonudeLokala.StatusPonudeLokala.REZERVISAN
        assert ponuda_lokala.odobrenje_kupovine_lokala == True
        assert lokal.status_prodaje_lokala == Lokali.StatusProdajeLokala.REZERVISAN

        url_kreiraj_novu_ponudu_lokala = reverse('ponude-lokali:kreiraj_ponudu_lokala')

        response_kreiraj_novu_ponudu_lokala = client.post(
            url_kreiraj_novu_ponudu_lokala,
            data=nova_ponuda_lokala_potencijalan,
            content_type='application/json'
        )
        assert response_kreiraj_novu_ponudu_lokala.status_code == 201

        # Nova Ponuda Lokala - POTENCIJALAN
        nova_ponuda_lokala = PonudeLokala.objects.first()
        izmenjen_lokal = Lokali.objects.filter(id_lokala__exact=nova_ponuda_lokala.lokali.id_lokala).first()

        # Provera statusa nove Ponude Lokala (Treba da je: "POTENCIJALAN"),
        # odobrenja (False)
        # i statusa Prodaje Lokala (Treba da ostane: "REZERVISAN")
        assert nova_ponuda_lokala.status_ponude_lokala == PonudeLokala.StatusPonudeLokala.POTENCIJALAN
        assert nova_ponuda_lokala.odobrenje_kupovine_lokala == False
        assert izmenjen_lokal.status_prodaje_lokala == Lokali.StatusProdajeLokala.REZERVISAN

        url_obrisi_novu_ponudu_lokala = reverse(
            'ponude-lokali:obrisi_ponudu_lokala',
            args=[nova_ponuda_lokala.id_ponude_lokala]
        )

        response = client.delete(url_obrisi_novu_ponudu_lokala)

        assert response.status_code == 204

        # Preostala prvobitna ponuda
        ponuda_lokala = PonudeLokala.objects.all().first()
        lokal = Lokali.objects.filter(id_lokala__exact=ponuda_lokala.lokali.id_lokala).first()

        # Provera Statusa Prodaje Lokala (Treba da je ostao: "REZERVISAN")
        assert lokal.status_prodaje_lokala == Lokali.StatusProdajeLokala.REZERVISAN

    def test_obrisi_ponudu_lokala_kupljen_status_lokala_rezervisan(self,
                                                                   client,
                                                                   nova_ponuda_lokala_status_kupljen_fixture,
                                                                   ):
        # TODO(Ivana): 1. Kreirati Ponudu Lokala koja je u statusu: "KUPLJEN" da bi status Lokala bio "KUPLJEN".
        # TODO(Ivana): 1. Kreirati Ponudu Lokala koja je u statusu: "REZERVISAN" da bi status Lokala bio "KUPLJEN".
        # TODO(Ivana): 2. Obrisati Ponudu Lokala status "KUPLJEN", i proveriti da li je Lokal ostao "REZERVISAN".
        """
        Kreiranje Ponude Lokala statusa 'KUPLJEN', da bi Status Prodaje Lokala bio PRODAT.
        Kreiranje nove Ponude Lokala statusa 'REZERVISAN', Status Prodaje Lokala ostaje PRODAT.
        Brisanje prve Ponude, da bi se proverilo da li Status Prodaje Lokala prelazi u REZERVISAN.
        """
        id_lokala = nova_ponuda_lokala_status_kupljen_fixture.lokali.id_lokala

        nova_ponuda_lokala_rezervisan = json.dumps(
            {
                "kupac_lokala": 1,
                "lokali": id_lokala,
                "cena_lokala_za_kupca": 54000,
                "napomena_ponude_lokala": 'string',
                "broj_ugovora_lokala": 'No56',
                "datum_ugovora_lokala": '5.2.2022',
                "status_ponude_lokala": PonudeLokala.StatusPonudeLokala.REZERVISAN,
                "nacin_placanja_lokala": 'Ceo iznos',
                "odobrenje_kupovine_lokala": True,
                "klijent_prodaje_lokala": 1
            }
        )

        # Prvobitna ponuda
        ponuda_lokala = PonudeLokala.objects.all().first()
        lokal = Lokali.objects.filter(id_lokala__exact=ponuda_lokala.lokali.id_lokala).first()

        # Status prvobitne Ponude Lokala (Treba da je "KUPLJEN") i odobrenje (True)
        # Status prvobitne Prodaje Lokala (Treba da je: "PRODAT")
        assert ponuda_lokala.status_ponude_lokala == PonudeLokala.StatusPonudeLokala.KUPLJEN
        assert ponuda_lokala.odobrenje_kupovine_lokala == True
        assert lokal.status_prodaje_lokala == Lokali.StatusProdajeLokala.PRODAT

        url_kreiraj_novu_ponudu_lokala = reverse('ponude-lokali:kreiraj_ponudu_lokala')

        response_kreiraj_novu_ponudu_lokala = client.post(
            url_kreiraj_novu_ponudu_lokala,
            data=nova_ponuda_lokala_rezervisan,
            content_type='application/json'
        )
        assert response_kreiraj_novu_ponudu_lokala.status_code == 201

        # Nova Ponuda Lokala - REZERVISAN
        nova_ponuda_lokala = PonudeLokala.objects.first()
        izmenjen_lokal = Lokali.objects.filter(id_lokala__exact=nova_ponuda_lokala.lokali.id_lokala).first()

        # Provera statusa nove Ponude Lokala (Treba da je: "REZERVISAN"),
        # odobrenja (True)
        # i statusa Prodaje Lokala (Treba da ostane: "PRODAT")
        assert nova_ponuda_lokala.status_ponude_lokala == PonudeLokala.StatusPonudeLokala.REZERVISAN
        assert nova_ponuda_lokala.odobrenje_kupovine_lokala == True
        assert izmenjen_lokal.status_prodaje_lokala == Lokali.StatusProdajeLokala.PRODAT

        # url_obrisi_novu_ponudu_lokala = reverse(
        #     'ponude-lokali:obrisi_ponudu_lokala',
        #     args=[nova_ponuda_lokala.id_ponude_lokala]
        # )
        #
        # response = client.delete(url_obrisi_novu_ponudu_lokala)
        #
        # assert response.status_code == 204
        #
        # # Preostala prvobitna ponuda
        # ponuda_lokala = PonudeLokala.objects.all().first()
        # lokal = Lokali.objects.filter(id_lokala__exact=ponuda_lokala.lokali.id_lokala).first()
        #
        # # Provera Statusa Prodaje Lokala (Treba da je ostao: "PRODAT")
        # assert lokal.status_prodaje_lokala == Lokali.StatusProdajeLokala.PRODAT

    def test_obrisi_sve_ponude_lokala_status_lokala_dostupan(self,
                                                             client,
                                                             nova_jedna_ponuda_lokala_fixture,
                                                             ):
        # TODO(Ivana): 1. Obrisati sve Ponude Lokala i Proveriti status Lokala (Treba da je dostupan)
        assert True


