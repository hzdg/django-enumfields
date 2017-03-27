import pytest

from .enums import Color
from .models import MyModel


@pytest.mark.django_db
def test_fields_value_is_enum_when_unsaved():
    obj = MyModel(color='r')
    assert Color.RED == obj.color


@pytest.mark.django_db
def test_fields_value_is_enum_when_saved():
    obj = MyModel(color='r')
    obj.save()
    assert Color.RED == obj.color


@pytest.mark.django_db
def test_fields_value_is_enum_when_created():
    obj = MyModel.objects.create(color='r')
    assert Color.RED == obj.color


@pytest.mark.django_db
def test_fields_value_is_enum_when_retrieved():
    MyModel.objects.create(color='r')
    obj = MyModel.objects.all()[:1][0]  # .first() not available on all Djangoes
    assert Color.RED == obj.color
