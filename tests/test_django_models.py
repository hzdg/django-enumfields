# -- encoding: UTF-8 --

from enum import IntEnum

import pytest
from django.db import connection

from .enums import Color, IntegerEnum, LabeledEnum, Taste, ZeroEnum
from .models import MyModel


@pytest.mark.django_db
def test_field_value():
    m = MyModel(color=Color.RED)
    m.save()
    assert m.color == Color.RED

    m = MyModel.objects.filter(color=Color.RED)[0]
    assert m.color == Color.RED

    # Passing the value should work the same way as passing the enum
    assert Color.RED.value == 'r'
    m = MyModel.objects.filter(color='r')[0]
    assert m.color == Color.RED

    with pytest.raises(ValueError):
        MyModel.objects.filter(color='xx')[0]


@pytest.mark.django_db
def test_db_value():
    m = MyModel(color=Color.RED)
    m.save()
    cursor = connection.cursor()
    cursor.execute('SELECT color FROM %s WHERE id = %%s' % MyModel._meta.db_table, [m.pk])
    assert cursor.fetchone()[0] == Color.RED.value


@pytest.mark.django_db
def test_enum_int_field_validators():
    if not hasattr(connection.ops, 'integer_field_range'):
        return pytest.skip('Needs connection.ops.integer_field_range')

    # Make sure that integer_field_range returns a range.
    # This is needed to make SQLite emulate a "real" db
    orig_method = connection.ops.integer_field_range
    connection.ops.integer_field_range = (lambda *args: (-100, 100))

    m = MyModel(color=Color.RED)

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
    m = MyModel(zero_field=ZeroEnum.ZERO,
                color=Color.GREEN)
    m.save()
    assert m.zero_field == ZeroEnum.ZERO

    m = MyModel.objects.get(id=m.id)
    assert m.zero_field == ZeroEnum.ZERO


@pytest.mark.django_db
def test_int_enum():
    m = MyModel(int_enum=IntegerEnum.A, color=Color.RED)
    m.save()

    m = MyModel.objects.get(id=m.id)
    assert m.int_enum == IntegerEnum.A
    assert isinstance(m.int_enum, IntegerEnum)


def test_serialization():
    from django.core.serializers.python import Serializer as PythonSerializer
    m = MyModel(color=Color.RED, taste=Taste.SALTY)
    ser = PythonSerializer()
    ser.serialize([m])
    fields = ser.getvalue()[0]["fields"]
    assert fields["color"] == m.color.value
    assert fields["taste"] == m.taste.value


@pytest.mark.django_db
def test_nonunique_label():
    obj = MyModel.objects.create(
        color=Color.BLUE,
        labeled_enum=LabeledEnum.FOOBAR
    )
    assert obj.labeled_enum is LabeledEnum.FOOBAR

    obj = MyModel.objects.get(pk=obj.pk)
    assert obj.labeled_enum is LabeledEnum.FOOBAR
