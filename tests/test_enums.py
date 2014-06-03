from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from enumfields import Enum
import pytest
from .models import MyModel
from .admin import MyModelAdmin, myadminsite
from django.http import HttpRequest
import mock


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

@pytest.mark.django_db
def test_choices_no_label():
    class Color(Enum):
        __order__ = 'RED GREEN'
        RED = 'r'
        GREEN = 'g'

        class Labels:
            RED = 'A custom label'

    COLOR_CHOICES = (
        ('r', 'A custom label'),
        ('g', 'Green')
    )

    assert Color.choices() == COLOR_CHOICES

@pytest.mark.django_db
def test_model_admin():
    mymodel_admin = MyModelAdmin(MyModel, myadminsite)
    mock_user = mock.MagicMock(autospec=User)
    mock_user.is_authenticated = mock.Mock(return_value=True)
    request = HttpRequest()
    request.REQUEST = {}
    request.user = mock_user
    request._dont_enforce_csrf_checks = True
    add_view = csrf_exempt(mymodel_admin.add_view)
    view = add_view(request)


