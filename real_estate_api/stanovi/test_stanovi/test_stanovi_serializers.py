from rest_framework.reverse import reverse


class TestStanovicSerijalizers:
    """Tesritanje Serijalizers STANOVI"""

    # TODO: (IVANA) Testirati serijalizer za STANOVE
    # @ SEE: TestKupciSerijalizers

    def test_invalid_serializers_detalji_jednog_stana(self,
                                                      client,
                                                      nova_dva_stana_fixture,
                                                      novi_autorizovan_korisnik_fixture_stanovi
                                                      ):
        """
        Testiranje serijalizera za pregled deatalja Stana koji ne postoji
        sa fixturom od dva kreirana nova Stana.

        Testiranje se vrsi sa autorizovanim Korisnikom sistema.

            * @see conftest.py (novi_autorizovan_korisnik_fixture_stanovi)
            * @see conftest.py (nova_dva_stana_fixture)

        @param client: A Django test client instance.
        @param nova_dva_stana_fixture: Stanovi
        @param novi_autorizovan_korisnik_fixture_stanovi: Korisnik
        """

        # Get invalid one Kupaca from Response
        url_detalji_stana_jedan = reverse('stanovi:detalji_stana', args=[nova_dva_stana_fixture[0].id_stana + 1000])
        response = client.get(url_detalji_stana_jedan)
        assert response.status_code == 404
