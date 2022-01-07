endpoint = '/kupci/'
auth_end_point = '/api/token/'


def test_sa_autorizovanim_korisnikom(client, django_user_model, novi_autorizovan_korisnik_fixture):
    response = client.get(endpoint)

    assert response.status_code == 200
