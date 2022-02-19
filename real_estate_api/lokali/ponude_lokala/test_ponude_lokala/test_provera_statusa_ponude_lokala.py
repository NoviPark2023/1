from real_estate_api.lokali.ponude_lokala.models import PonudeLokala


class TestPromenaStatusLokalaIzPonudeLokala:
    """Testiranje promene Statusa Ponude Lokala u PONUDAMA LOKALA"""

    def test_da_li_su_tri_ponuda_lokala_kreirane(self, nove_tri_ponude_lokala_fixture):
        """ Test da li su tri Ponude Lokala kreirane u bazi. """

        broj_ponuda_lokala_from_db = PonudeLokala.objects.all().count()
        assert broj_ponuda_lokala_from_db == 3

        # TODO: Finish implement testing.
