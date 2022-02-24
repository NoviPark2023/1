from rest_framework.reverse import reverse

from real_estate_api.korisnici.models import Korisnici
from real_estate_api.lokali.ponude_lokala.models import PonudeLokala


class TestRestApiUrlsReports:
    """Testitanje API URLs Endpointa Reports-a Lokala"""

    def test_sa_neautorizovanim_korisnikom(self, client, novi_neautorizovan_korisnik_fixture_reports_lok):
        """
        Direktan poziv bez autorizacije endpointa:
            * 'reports-lokali:reports-lokali'
            * 'reports-lokali:reports-lokali-po-korisniku'
            * 'reports-lokali:reports-lokali-po-klijentu'
            * 'reports-lokali:reports-roi'

        ---
        @param client: A Django test client instance.
        @return status code 401: Unauthorized for all API endpoints.
        """

        url_izvestaj_svi_lokali = reverse('reports-lokali:reports-lokali')
        url_reports_po_korisniku = reverse('reports-lokali:reports-lokali-po-korisniku')
        url_reports_lokali_po_klijentu = reverse('reports-lokali:reports-lokali-po-klijentu')
        url_reports_roi_lokala = reverse('reports-lokali:reports-roi')

        response = client.get(url_izvestaj_svi_lokali)
        assert response.status_code == 401

        response = client.get(url_reports_po_korisniku)
        assert response.status_code == 401

        response = client.get(url_reports_lokali_po_klijentu)
        assert response.status_code == 401

        response = client.get(url_reports_roi_lokala)
        assert response.status_code == 401

    def test_sa_autorizovanim_korisnikom(self,
                                         client,
                                         novi_autorizovan_korisnik_fixture_reports_lok
                                         ):
        """
        Direktan poziv sa autorizovanim Korisnikom endpointa:
            * 'reports-lokali:reports-lokali'
            * 'reports-lokali:reports-lokali-po-korisniku'
            * 'reports-lokali:reports-lokali-po-klijentu'

        * @see conftest.py (novi_autorizovan_korisnik_fixture_reports_lok)

        ---
        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_reports_lok: Obican Korisnik sa autorizacijom.
        @return status code 200: OK
        """

        url_izvestaj_svi_lokali = reverse('reports-lokali:reports-lokali')
        url_reports_po_korisniku = reverse('reports-lokali:reports-lokali-po-korisniku')
        url_reports_lokali_po_klijentu = reverse('reports-lokali:reports-lokali-po-klijentu')

        response = client.get(url_izvestaj_svi_lokali)
        assert response.status_code == 200

        response = client.get(url_reports_po_korisniku)
        assert response.status_code == 200

        response = client.get(url_reports_lokali_po_klijentu)
        assert response.status_code == 200

    def test_kreiranje_izvestaja_za_entitet_lokali(self, client,
                                                   nove_tri_ponude_lokala_fixture_reporti,
                                                   novi_izvestaj_lokali_statistika_fixture,
                                                   ):
        """
        Test poziv endpointa: 'reports-lokali:reports-lokali', sa autorizovanim Korisnikom.
        Takodje se proverava i Response sadrzaj.
        Autorizacije Korisnika se vrsi u 'nove_tri_ponude_lokala_fixture_reporti'.

            * @see  reports_lokali.test_reports_lokali.conftest.py (nove_tri_ponude_lokala_fixture_reporti)
            * @see reports_lokali.test_reports_lokali.conftest.py (novi_izvestaj_lokali_statistika_fixture)

        ---
        @param client: A Django test client instance.
        @param novi_izvestaj_lokali_statistika_fixture: Mock Reporta.
        @param nove_tri_ponude_lokala_fixture_reporti: Mock 3 PonudeLokala.
        @return status code 200: HTTP OK
        """
        url_izvestaj_svi_lokali = reverse('reports-lokali:reports-lokali')

        response = client.get(url_izvestaj_svi_lokali, args=novi_izvestaj_lokali_statistika_fixture)

        assert response.status_code == 200

        assert response.json() == {
            "ukupno_lokala": novi_izvestaj_lokali_statistika_fixture.ukupno_lokala,
            "rezervisano": novi_izvestaj_lokali_statistika_fixture.rezervisano,
            "dostupno": novi_izvestaj_lokali_statistika_fixture.dostupno,
            "prodato": novi_izvestaj_lokali_statistika_fixture.prodato,
            "procenat_rezervisanih": novi_izvestaj_lokali_statistika_fixture.procenat_rezervisanih,
            "procenat_dostupnih": novi_izvestaj_lokali_statistika_fixture.procenat_dostupnih,
            "procenat_prodatih": novi_izvestaj_lokali_statistika_fixture.procenat_prodatih,
            "prodaja_po_mesecima": novi_izvestaj_lokali_statistika_fixture.prodaja_po_mesecima,
            "broj_ponuda_po_mesecima": novi_izvestaj_lokali_statistika_fixture.broj_ponuda_po_mesecima,
            "ukupna_suma_prodatih_lokala": novi_izvestaj_lokali_statistika_fixture.ukupna_suma_prodatih_lokala
        }

    def test_prodaja_lokala_po_korisniku(self, client,
                                         nove_tri_ponude_lokala_fixture_reporti,
                                         novi_autorizovan_korisnik_fixture_reports_lok
                                         ):
        """
        Testiranje endpointa ROI Lokala: 'reports-lokali:reports-lokali-po-korisniku'.
        Reponse vraća sumiran broj prodatih Lokala po Korisniku sistema (Prodavcu) i
        podatke samog Korisnika.

            * @see reports_lokali.test_reports_lokali.conftest.py (nove_tri_ponude_lokala_fixture_reporti)
            * @see reports_lokali.test_reports_lokali.conftest.py (novi_autorizovan_korisnik_fixture_reports_lok)

        ---
        :param client: A Django test client instance.
        :param nove_tri_ponude_lokala_fixture_reporti:  Mock 3 PonudeLokala.
        :param novi_autorizovan_korisnik_fixture_reports_lok: Obican Korisnik sa autorizacijom.
        """
        url_prodaja_lokala_po_korisniku = reverse('reports-lokali:reports-lokali-po-korisniku')

        # Broj autorizovanih Korisnika
        assert Korisnici.objects.all().count() == 1

        # Broj Ponuda Lokala
        assert PonudeLokala.objects.all().count() == 3

        response = client.get(url_prodaja_lokala_po_korisniku)

        assert response.status_code == 200

        assert response.json() == \
               [
                   {
                       "id": novi_autorizovan_korisnik_fixture_reports_lok.id,
                       "ime": novi_autorizovan_korisnik_fixture_reports_lok.ime,
                       "prezime": novi_autorizovan_korisnik_fixture_reports_lok.prezime,
                       "email": novi_autorizovan_korisnik_fixture_reports_lok.email,
                       "role": novi_autorizovan_korisnik_fixture_reports_lok.role,
                       "prodati_lokali_korisnici": 1
                   }
               ]

    def test_prodaja_lokala_po_klijentu(self, client,
                                        nove_tri_ponude_lokala_fixture_reporti,
                                        novi_kupac_fixture_reporti_lok,
                                        ):
        """
        Testiranje endpointa ROI Lokala: 'reports-lokali:reports-lokali-po-klijentu'.
        Reponse vraća statistiku Lokala po Klijentu(Kupcu) i to:
            * prodati_lokali_klijenti
            * rezervisani_lokali_klijenti
            * potencijalni_lokali_klijenti

        Autorizovan Korisnik se registruje u 'nove_tri_ponude_lokala_fixture_reporti' fixturi.


            * @see reports_lokali.test_reports_lokali.conftest.py (nove_tri_ponude_lokala_fixture_reporti)
            * @see reports_lokali.test_reports_lokali.conftest.py (novi_kupac_fixture_reporti_lok)


        ---
        :param client: A Django test client instance.
        :param nove_tri_ponude_lokala_fixture_reporti: Mock 3 PonudeLokala.
        :param novi_kupac_fixture_reporti_lok: Mock jednog Kupca.
        """
        url_prodaja_lokala_po_klijentu = reverse('reports-lokali:reports-lokali-po-klijentu')

        response = client.get(url_prodaja_lokala_po_klijentu)

        assert response.status_code == 200

        assert response.json() == \
               [
                   {
                       "id_kupca": novi_kupac_fixture_reporti_lok.id_kupca,
                       "ime_prezime": novi_kupac_fixture_reporti_lok.ime_prezime,
                       "email": novi_kupac_fixture_reporti_lok.email,
                       "prodati_lokali_klijenti": 1,
                       "rezervisani_lokali_klijenti": 1,
                       "potencijalni_lokali_klijenti": 1
                   }
               ]

    def test_return_on_investment(self, client,
                                  novi_autorizovan_korisnik_fixture_reports_lok,
                                  novi_lokal_1_fixture,
                                  novi_lokal_2_fixture,
                                  novi_lokal_3_fixture,
                                  novi_izvestaj_roi_lokala,
                                  ):
        """
        Testiranje endpointa ROI Lokala: 'reports-lokali:reports-roi'.
        ROI Lokala obuhvata tri celine i to:
            * kvadratura_lokala
            * ukupna_cena_lokala_po_lamelama
            * ukupan_roi_lokala

        :param client: A Django test client instance.
        :param novi_autorizovan_korisnik_fixture_reports_lok: Obican Korisnik sa autorizacijom.
        :param novi_lokal_1_fixture: Jedan entitet Lokala fixture.
        :param novi_lokal_2_fixture: Jedan entitet Lokala fixture.
        :param novi_lokal_3_fixture: Jedan entitet Lokala fixture.
        :param novi_izvestaj_roi_lokala: Roi izvestaj Lokala
        """
        url_return_on_investment = reverse('reports-lokali:reports-roi')

        response = client.get(url_return_on_investment, args=novi_izvestaj_roi_lokala)

        assert response.status_code == 200

        print(f' FIXTURE RESPONSE: {novi_izvestaj_roi_lokala}')

        assert response.json() == {
            "kvadratura_lokala": novi_izvestaj_roi_lokala.kvadratura_lokala,
            "ukupna_cena_lokala_po_lamelama": novi_izvestaj_roi_lokala.ukupna_cena_lokala_po_lamelama,
            "ukupan_roi_lokala": novi_izvestaj_roi_lokala.ukupan_roi_lokala
        }
