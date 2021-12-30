import pytest

from real_estate_api.stanovi.models import Stanovi


@pytest.mark.django_db
def test_create_category():
    category = Stanovi.objects.create(id_stana=1)
    assert category.id_stana == 1
