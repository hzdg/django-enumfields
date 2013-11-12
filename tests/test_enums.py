from django.db import connection
from enumfields import Enum
import pytest
from .models import MyModel


def test_choices():
    class Color(Enum):
        __order__ = 'RED GREEN BLUE'

        RED = 'r'
        GREEN = 'g'
        BLUE = 'b'

    COLOR_CHOICES = (
        ('r', 'Red'),
        ('g', 'Green'),
        ('b', 'Blue'),
    )
    assert Color.choices() == COLOR_CHOICES


def test_labels():
    class Color(Enum):
        RED = 'r'
        GREEN = 'g'

        class Labels:
            RED = 'A custom label'

    assert Color.RED.label == 'A custom label'
    assert Color.GREEN.label == 'Green'


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
