import pytest

from .models import MyModel

try:
    from .enums import Color  # Use the new location of Color enum
except ImportError:
    Color = MyModel.Color  # Attempt the 0.7.4 location of color enum


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
