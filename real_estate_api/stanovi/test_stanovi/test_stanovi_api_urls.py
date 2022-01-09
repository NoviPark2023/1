from rest_framework.reverse import reverse


class TestRestApiUrlsStanovi:
    """Testitanje API URLs Endpointa entiteta Stanovi"""

    def test_sa_ne_autorizovanim_korisnikom(self, client):
        """
        Test poziv 'endpoint_svi_kupci' -a sa ne autorizovanim Korisnikom.

            * @see conftest.py (novi_korisnik_ne_autorizovan_fixture)

        @param client: A Django test client instance.
        @return status code 401: Unauthorized
        """

        url_svi_stanovi = reverse('stanovi:lista_stanova')

        response = client.get(url_svi_stanovi)

        assert response.status_code == 401

    def test_sa_autorizovanim_korisnikom(self, client, novi_autorizovan_korisnik_fixture_stanovi):
        """
        Test poziv 'endpoint_svi_kupci' -a sa autorizovanim Korisnikom.

            * @see conftest.py (novi_autorizovan_korisnik_fixture)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_stanovi: Obican Korisnik sa autorizacijom.
        @return status code 200: OK
        """

        url_svi_stanovi = reverse('stanovi:lista_stanova')

        response = client.get(url_svi_stanovi)

        assert response.status_code == 200

    # TODO: (IVANA) OVE PUTANJE TREBA TESTIRATI.
    """
    # Lista svih Stanova
    path('', ListaStanovaAPIView.as_view(), name='lista_stanova'),
    # Detalji Stana
    path('detalji-stana/<int:id_stana>', StanoviDetaljiAPIVIew.as_view(), name='detalji_stana'),
    # Kreiranje Stana
    path('kreiraj-stan', KreirajStanAPIView.as_view(), name='kreiraj_stan'),
    # Uredjivanje Stana
    path('izmeni-stan/<int:id_stana>', UrediStanViewAPI.as_view(), name='izmeni_stan'),
    # Brisanje Stana
    path('obrisi-stan/<int:id_stana>', ObrisiStanViewAPI.as_view(), name='obrisi_stan'),
    # Broj Ponuda za Stan po mesecima
    path('ponude-stana-meseci/<int:id_stana>', BrojPonudaStanovaPoMesecimaAPIView.as_view(), name='ponude-stana-meseci'),
    # Lista svih mesecnih cena kvadrata
    path('listing-cena-kvadrata', AzuriranjeCenaStanaAPIView.as_view(), name='kreiraj-cenu-kvadrata'),
    # Kreiranje mesecne cene kvadrata
    path('kreiraj-cenu-kvadrata', AzuriranjeCenaCreateAPIView.as_view(), name='kreiraj-cenu-kvadrata'),
    # Promena mesecne cene kvadrata
    path('promeni-cenu-kvadrata/<int:id_azur_cene>', AzuriranjeCenaUpdateAPIView.as_view(), name='promeni-cenu-kvadrata'),
    # Brisanje mesecne cene kvadrata
    path('izbrisi-cenu-kvadrata/<int:id_azur_cene>', AzuriranjeCenaDeleteAPIView.as_view(), name='izbrisi-cenu-kvadrata')
    """

    def test_lista_svih_stanova_url_autorizovan_korisnik(self, client, novi_autorizovan_korisnik_fixture_stanovi):
        """
        Test poziv 'lista_stanova' -a sa autorizovanim Korisnikom.

            * @see conftest.py (novi_autorizovan_korisnik_fixture_stanovi)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_stanovi: Autorizovan Korisnik .
        @return status code 200: OK
        """

        url_svi_stanovi = reverse('stanovi:lista_stanova')

        response = client.get(url_svi_stanovi)

        assert response.status_code == 200  # (HTTP) 200 Authorized.

    def test_lista_svih_stanova_url_ne_autorizovan_korisnik(self, client, novi_korisnik_ne_autorizovan_fixture_stanovi):
        """
        Test poziv 'lista_stanova' -a sa ne autorizovanim Korisnikom ((HTTP) 401 Unauthorized).

            * @see conftest.py (novi_korisnik_ne_autorizovan_fixture_stanovi)

        @param client: A Django test client instance.
        @param novi_korisnik_ne_autorizovan_fixture_stanovi: Obican Korisnik bez autorizacie.
        @return status code 401:  Unauthorized
        """

        url_svi_stanovi = reverse('stanovi:lista_stanova')

        response = client.get(url_svi_stanovi)

        assert response.status_code == 401  # (HTTP) 401 Unauthorized.
