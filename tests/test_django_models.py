# -- encoding: UTF-8 --

import pytest
from django.db import connection
from enum import IntEnum

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
def test_enum_int_field_validators():
    if not hasattr(connection.ops, 'integer_field_range'):
        return pytest.skip('Needs connection.ops.integer_field_range')

    # Make sure that integer_field_range returns a range.
    # This is needed to make SQLite emulate a "real" db
    orig_method = connection.ops.integer_field_range
    connection.ops.integer_field_range = (lambda *args: (-100, 100))

    m = MyModel(color=MyModel.Color.RED)

    # Uncache validators property of taste_int
    for f in m._meta.fields:
        if f.name == 'taste_int':
            if 'validators' in f.__dict__:
                del f.__dict__['validators']

    # Run the validators
    m.full_clean()

    # Revert integer_field_range method
    connection.ops.integer_field_range = orig_method


@pytest.mark.django_db
def test_zero_enum_loads():
    # Verifies that we can save and load enums with the value of 0 (zero).
    m = MyModel(zero_field=MyModel.ZeroEnum.ZERO,
                color=MyModel.Color.GREEN)
    m.save()
    assert m.zero_field == MyModel.ZeroEnum.ZERO

    m = MyModel.objects.get(id=m.id)
    assert m.zero_field == MyModel.ZeroEnum.ZERO


@pytest.mark.django_db
def test_int_enum():
    m = MyModel(int_enum=MyModel.IntegerEnum.A, color=MyModel.Color.RED)
    m.save()

    m = MyModel.objects.get(id=m.id)
    assert m.int_enum == MyModel.IntegerEnum.A
    assert isinstance(m.int_enum, MyModel.IntegerEnum)


def test_serialization():
    from django.core.serializers.python import Serializer as PythonSerializer
    m = MyModel(color=MyModel.Color.RED, taste=MyModel.Taste.SALTY)
    ser = PythonSerializer()
    ser.serialize([m])
    fields = ser.getvalue()[0]["fields"]
    assert fields["color"] == m.color.value
    assert fields["taste"] == m.taste.value
