import pytest
from faker import Faker
import json

from real_estate_api.korisnici.models import Korisnici
from real_estate_api.stanovi.models import Stanovi, AzuriranjeCena

fake = Faker()


# region FIXTURE NE REGISTROVAN KORISNIK STANOVI
@pytest.fixture()
def novi_korisnik_neautorizovan_fixture_stanovi(db) -> Korisnici:
    return Korisnici.objects.create(
        username='nikola',
        password='nikola',
        email='nikola@nikola.com',
        ime='Nikola',
        prezime='Nikola',
    )


# endregion

# region FIXTURE REGISTROVAN KORISNIK STANOVI
@pytest.fixture(autouse=False)
def novi_autorizovan_korisnik_fixture_stanovi(db, client, django_user_model) -> Korisnici:
    """
    Kreiranje novog Korisnika i autorizacija istog na sistem.

    @param db: Testna DB.
    @param client: A Django test client instance.
    @param django_user_model: Korisnik.
    @return: Entitet autorizovan Korisnik.
    """

    korisnik = Korisnici.objects.create(
        username='nikola',
        password='nikola',
        email='nikola@nikola.com',
        ime='Nikola',
        prezime='Nikola',
    )

    client.force_login(korisnik)

    return korisnik


# endregion

# region AZURIRANJE CENA Stanov
@pytest.fixture(autouse=False)
def kreiraj_tri_auriranja_cena_stanovi(db) -> list[AzuriranjeCena]:
    """
    Separaciona tabela 'Azuriranje Cena Stanova' koja se koristi za Automatsko
    racunanje cene stanova na osnovu zadatih parametara.

    @param db: Testna DB
    @return: AzuriranjeCena obj.
    """
    azuriranje_cena = AzuriranjeCena.objects.bulk_create(
        [
            AzuriranjeCena(id_azur_cene=1,
                           sprat="1.0",
                           broj_soba=2,
                           orijentisanost="Jug",
                           cena_kvadrata=1568.00
                           ),
            AzuriranjeCena(id_azur_cene=2,
                           sprat="1.0",
                           broj_soba=3,
                           orijentisanost="Jug",
                           cena_kvadrata=1574.66
                           ),
            AzuriranjeCena(id_azur_cene=3,
                           sprat="1.0",
                           broj_soba=3,
                           orijentisanost="Jug",
                           cena_kvadrata=1568.00
                           ),
        ]
    )

    return azuriranje_cena


# endregion

# region NOVO AZURIRANJE CENA FIXTURE
@pytest.fixture(autouse=False)
def novo_azuriranje_cena_fixture(db):
    """
    Kreiranje novog Azuriranja cena.

    @param db: Testna DB.
    @return: Entitet 'Azuriranje cena'.
    """
    azuriranje_cena = AzuriranjeCena.objects.create(
        id_azur_cene=1,
        sprat="1.0",
        broj_soba=3,
        orijentisanost="Jug",
        cena_kvadrata=1568.00
    )

    return azuriranje_cena


# endregion

# region FIXTURE JSON DUMP AZURIRANJE CENA
@pytest.fixture(autouse=False)
def novo_azuriranje_cena_json_fixture():
    return json.dumps(
        {
            "id_azur_cene": 5,
            "sprat": "2.0",
            "broj_soba": 2,
            "orijentisanost": "Jug",
            "cena_kvadrata": 1500.00,
        }
    )


# endregion

# region NOVI JEDAN STAN FIXTURE
@pytest.fixture(autouse=False)
def novi_jedan_stan_fixture_stanovi(db, kreiraj_tri_auriranja_cena_stanovi) -> Stanovi:
    """
    Kreiranje novog Stana.

    @param kreiraj_auriranje_cena:  pytest.fixture (kreiraj_tri_auriranja_cena_stanovi)
    @param db: Testna DB.
    @return: Entitet 'Stanovi'.
    """

    stan = Stanovi.objects.create(
        id_stana=1,
        lamela="L3.1.S2",
        adresa_stana="Adresa Stana L3.1.S2",
        kvadratura='48.02',
        kvadratura_korekcija='46.58',
        iznos_za_korekciju_kvadrature='0.97',
        sprat="1.0",
        broj_soba=2,
        orijentisanost="Jug",
        broj_terasa=0,
        unesena_mauelna_cena_stana=False,
        cena_stana="73.036,499",
        cena_kvadrata="1568.00",
        napomena='Nema napomene',
        status_prodaje="dostupan",
    )

    return stan


# endregion

# region NOVA DVA STANA FIXTURE
@pytest.fixture(autouse=False)
def nova_dva_stana_fixture(db, kreiraj_tri_auriranja_cena_stanovi) -> Stanovi:
    """
    Kreiranje novog Stana.

    @param kreiraj_auriranje_cena:  pytest.fixture (kreiraj_tri_auriranja_cena_stanovi)
    @param db: Testna DB.
    @return: Entitet 'Stanovi'.
    """
    stanovi = Stanovi.objects.bulk_create(
        [
            Stanovi(
                id_stana=1,
                lamela="L2.1.S10",
                adresa_stana="Adresa Stana L2.1.S10",
                kvadratura=67.49,
                kvadratura_korekcija=65.47,
                iznos_za_korekciju_kvadrature=0.97,
                sprat="1.0",
                broj_soba=3,
                orijentisanost="Jug",
                broj_terasa="0",
                unesena_mauelna_cena_stana=False,
                cena_stana="103085.59",
                cena_kvadrata="1574.66",
                napomena='Nema napomene',
                status_prodaje="dostupan",
            ),
            Stanovi(
                id_stana=2,
                lamela="L3.1.S1",
                adresa_stana="Adresa Stana L3.1.S1",
                kvadratura=50.25,
                kvadratura_korekcija=48.74,
                iznos_za_korekciju_kvadrature=0.97,
                sprat="1.0",
                broj_soba=3,
                orijentisanost="Jug",
                broj_terasa="1",
                unesena_mauelna_cena_stana=False,
                cena_stana="76428.24",
                cena_kvadrata="1568.00",
                napomena='Nema napomene',
                status_prodaje="dostupan",
            )
        ]

    )

    return stanovi


# endregion

# region FIXTURE JSON DUMP JEDAN STAN
@pytest.fixture(autouse=False)
def novi_jedan_stan_json_fixture():
    return json.dumps(
        {
            "id_stana": 5,
            "lamela": "L2.1.S10",
            "adresa_stana": "Adresa Stana L2.1.S10",
            "kvadratura": 48.02,
            "kvadratura_korekcija": 46.58,
            "iznos_za_korekciju_kvadrature": 0.97,
            "sprat": "1.0",
            "broj_soba": 2,
            "orijentisanost": "Jug",
            "broj_terasa": "1",
            "unesena_mauelna_cena_stana": False,
            "cena_stana": "73036.50",
            "cena_kvadrata": "1568.00",
            "napomena": 'Nema napomene',
            "status_prodaje": "dostupan",
        }
    )


# endregion

# region FIXTURE JSON DUMP DVA STANA
@pytest.fixture(autouse=False)
def nova_dva_stana_json_fixture():
    return json.dumps(
        [
            {
                "id_stana": 5,
                "lamela": "L2.1.S10",
                "adresa_stana": "Adresa Stana L2.1.S10",
                "kvadratura": 67.49,
                "kvadratura_korekcija": 65.47,
                "iznos_za_korekciju_kvadrature": 0.97,
                "sprat": "1.0",
                "broj_soba": 3,
                "orijentisanost": "Jug",
                "broj_terasa": "0",
                "unesena_mauelna_cena_stana": False,
                "cena_stana": "103085.59",
                "cena_kvadrata": "1574.66",
                "napomena": 'Nema napomene',
                "status_prodaje": "dostupan",
            },
            {
                "id_stana": 6,
                "lamela": "L3.1.S1",
                "adresa_stana": "Adresa Stana L3.1.S1",
                "kvadratura": 50.25,
                "kvadratura_korekcija": 48.74,
                "iznos_za_korekciju_kvadrature": 0.97,
                "sprat": "1.0",
                "broj_soba": 3,
                "orijentisanost": "Jug",
                "broj_terasa": "1",
                "unesena_mauelna_cena_stana": False,
                "cena_stana": "76428.24",
                "cena_kvadrata": "1568.00",
                "napomena": 'Nema napomene',
                "status_prodaje": "dostupan",
            }
        ]
    )


# endregion

# region FIXTURE JSON DUMP JEDAN NEVALIDAN STAN
@pytest.fixture(autouse=False)
def novi_jedan_nevalidan_stan_json_fixture():
    return json.dumps(
        {
            'id_stana': 3,
            'lamela': "L4.1.S2",
            'adresa_stana': "Adresa Stana L3.1.S2",
            'kvadratura': '48.02',
            'kvadratura_korekcija': 46.58,
            'iznos_za_korekciju_kvadrature': '0.97',
            'sprat': 1.0,
            'broj_soba': 2,
            'orijentisanost': "Jug",
            'broj_terasa': -2,
            "unesena_mauelna_cena_stana": False,
            'cena_stana': "73036.50",
            'cena_kvadrata': "1568.00",
            'napomena': 'Nema napomene',
            'status_prodaje': "dostupan"
        }
    )


# endregion

# region FIXTURE JSON DUMP DVA STANA UNIQUIE LAMELA ERROR
@pytest.fixture(autouse=False)
def nova_dva_stana_sa_istom_lamelom_json_fixture():
    return json.dumps(
        [
            {
                "id_stana": 5,
                "lamela": "L2.1.S10",
                "adresa_stana": "Adresa Stana L2.1.S10",
                "kvadratura": 67.49,
                "kvadratura_korekcija": 65.47,
                "iznos_za_korekciju_kvadrature": 0.97,
                "sprat": "1.0",
                "broj_soba": 3,
                "orijentisanost": "Jug",
                "broj_terasa": "0",
                "unesena_mauelna_cena_stana": False,
                "cena_stana": "103085.59",
                "cena_kvadrata": "1574.66",
                "napomena": 'Nema napomene',
                "status_prodaje": "dostupan",
            },
            {
                "id_stana": 6,
                "lamela": "L2.1.S10",
                "adresa_stana": "Adresa Stana L3.1.S1",
                "kvadratura": 50.25,
                "kvadratura_korekcija": 48.74,
                "iznos_za_korekciju_kvadrature": 0.97,
                "sprat": "1.0",
                "broj_soba": 3,
                "orijentisanost": "Jug",
                "broj_terasa": "1",
                "unesena_mauelna_cena_stana": False,
                "cena_stana": "76428.24",
                "cena_kvadrata": "1568.00",
                "napomena": 'Nema napomene',
                "status_prodaje": "dostupan",
            }
        ]
    )

# endregion
