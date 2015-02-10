# -- encoding: UTF-8 --

import uuid

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.db import connection
from django.forms import BaseForm
from django.test import Client
from django.utils.translation import ugettext_lazy
import pytest
from enumfields import Enum, EnumField, EnumIntegerField
from .models import MyModel
import six


class Color(Enum):
    __order__ = 'RED GREEN BLUE'

    GREEN = 'g'
    RED = 'r'
    BLUE = 'b'

    class Labels:
        RED = 'Reddish'
        BLUE = ugettext_lazy(u'bluë')


def test_choice_ordering():
    EXPECTED_CHOICES = (
        ('r', 'Reddish'),
        ('g', 'Green'),
        ('b', u'bluë'),
    )
    for ((ex_key, ex_val), (key, val)) in zip(EXPECTED_CHOICES, Color.choices()):
        assert key == ex_key
        assert six.text_type(val) == six.text_type(ex_val)

def test_custom_labels():
    # Custom label
    assert Color.RED.label == 'Reddish'
    assert six.text_type(Color.RED) == 'Reddish'

def test_automatic_labels():
    # Automatic label
    assert Color.GREEN.label == 'Green'
    assert six.text_type(Color.GREEN) == 'Green'

def test_lazy_labels():
    # Lazy label
    assert isinstance(six.text_type(Color.BLUE), six.string_types)
    assert six.text_type(Color.BLUE) == u'bluë'

def test_formfield_labels():
    # Formfield choice label
    form_field = EnumField(Color).formfield()
    expectations = dict((val.value, six.text_type(val)) for val in Color)
    for value, text in form_field.choices:
        if value:
            assert text == expectations[value]

def test_formfield_functionality():
    form_cls = type("FauxForm", (BaseForm,), {
        "base_fields": {"color": EnumField(Color).formfield()}
    })
    form = form_cls(data={"color": "r"})
    assert not form.errors
    assert form.cleaned_data["color"] == Color.RED


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


@pytest.fixture
def client():
    return Client()


SUPERUSER_USERNAME = "superuser"
SUPERUSER_PASS = "superpass"


@pytest.fixture
def superuser():
    return get_user_model().objects.create_superuser(username=SUPERUSER_USERNAME, password=SUPERUSER_PASS,
                                                     email="billgates@microsoft.com")


@pytest.fixture
def superuser_client(client, superuser):
    client.login(username=SUPERUSER_USERNAME, password=SUPERUSER_PASS)
    return client


@pytest.mark.django_db
@pytest.mark.urls('tests.urls')
def test_model_admin(superuser_client):
    url = reverse("admin:tests_mymodel_add")
    secret_uuid = str(uuid.uuid4())
    post_data = {
        'color': MyModel.Color.RED.value,
        'taste': MyModel.Taste.UMAMI.value,
        'taste_int': MyModel.Taste.SWEET.value,
        'random_code': secret_uuid
    }
    response = superuser_client.post(url, follow=True, data=post_data)
    response.render()
    text = response.content

    assert b"This field is required" not in text
    assert b"Select a valid choice" not in text
    try:
        inst = MyModel.objects.get(random_code=secret_uuid)
    except MyModel.DoesNotExist:
        assert False, "Object wasn't created in the database"
    assert inst.color == MyModel.Color.RED, "Redness not assured"
    assert inst.taste == MyModel.Taste.UMAMI, "Umami not there"
    assert inst.taste_int == MyModel.Taste.SWEET, "Not sweet enough"


def test_django_admin_lookup_value_for_integer_enum_field():
    field = EnumIntegerField(MyModel.Taste)

    assert field.get_prep_value(str(MyModel.Taste.BITTER)) == 3, "get_prep_value should be able to convert from strings"


@pytest.mark.django_db
def test_zero_enum_loads():
    # Verifies that we can save and load enums with the value of 0 (zero).
    m = MyModel(zero_field=MyModel.ZeroEnum.ZERO,
                color=MyModel.Color.GREEN)
    m.save()
    assert m.zero_field == MyModel.ZeroEnum.ZERO

    m = MyModel.objects.get(id=m.id)
    assert m.zero_field == MyModel.ZeroEnum.ZERO
