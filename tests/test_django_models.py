# -- encoding: UTF-8 --

from django.db import connection
import pytest
from .models import MyModel


@pytest.mark.django_db
def test_field_value():
    m = MyModel(color=MyModel.Color.RED)
    m.save()
    assert m.color == MyModel.Color.RED

    m = MyModel.objects.filter(color=MyModel.Color.RED)[0]
    assert m.color == MyModel.Color.RED


@pytest.mark.django_db
def test_db_value():
    m = MyModel(color=MyModel.Color.RED)
    m.save()
    cursor = connection.cursor()
    cursor.execute('SELECT color FROM %s WHERE id = %%s' % MyModel._meta.db_table, [m.pk])
    assert cursor.fetchone()[0] == MyModel.Color.RED.value


@pytest.mark.django_db
def test_zero_enum_loads():
    # Verifies that we can save and load enums with the value of 0 (zero).
    m = MyModel(zero_field=MyModel.ZeroEnum.ZERO,
                color=MyModel.Color.GREEN)
    m.save()
    assert m.zero_field == MyModel.ZeroEnum.ZERO

    m = MyModel.objects.get(id=m.id)
    assert m.zero_field == MyModel.ZeroEnum.ZERO
