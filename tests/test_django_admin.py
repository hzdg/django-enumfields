# -- encoding: UTF-8 --
import re
import uuid

import pytest
try:
    from django.core.urlresolvers import reverse  # Django 1.x
except ImportError:
    from django.urls import reverse  # Django 2.x

from enumfields import EnumIntegerField

from .enums import Color, IntegerEnum, Taste, ZeroEnum
from .models import MyModel


@pytest.mark.django_db
@pytest.mark.urls('tests.urls')
def test_model_admin_post(admin_client):
    url = reverse("admin:tests_mymodel_add")
    secret_uuid = str(uuid.uuid4())
    post_data = {
        'color': Color.RED.value,
        'taste': Taste.UMAMI.value,
        'taste_int': Taste.SWEET.value,
        'random_code': secret_uuid,
        'zero2': ZeroEnum.ZERO.value,
    }
    response = admin_client.post(url, follow=True, data=post_data)
    response.render()
    text = response.content

    assert b"This field is required" not in text
    assert b"Select a valid choice" not in text
    try:
        inst = MyModel.objects.get(random_code=secret_uuid)
    except DoesNotExist:
        assert False, "Object wasn't created in the database"
    assert inst.color == Color.RED, "Redness not assured"
    assert inst.taste == Taste.UMAMI, "Umami not there"
    assert inst.taste_int == Taste.SWEET, "Not sweet enough"


@pytest.mark.django_db
@pytest.mark.urls('tests.urls')
@pytest.mark.parametrize('q_color', (None, Color.BLUE, Color.RED))
@pytest.mark.parametrize('q_taste', (None, Taste.SWEET, Taste.SOUR))
@pytest.mark.parametrize('q_int_enum', (None, IntegerEnum.A, IntegerEnum.B))
def test_model_admin_filter(admin_client, q_color, q_taste, q_int_enum):
    """
    Test that various combinations of Enum filters seem to do the right thing in the change list.
    """

    # Create a bunch of objects...
    MyModel.objects.create(color=Color.RED)
    for taste in Taste:
        MyModel.objects.create(color=Color.BLUE, taste=taste)
    MyModel.objects.create(color=Color.BLUE, taste=Taste.UMAMI, int_enum=IntegerEnum.A)
    MyModel.objects.create(color=Color.GREEN, int_enum=IntegerEnum.B)

    # Build a Django lookup...
    lookup = dict((k, v) for (k, v) in {
        'color': q_color,
        'taste': q_taste,
        'int_enum': q_int_enum,
    }.items() if v is not None)
    # Build the query string (this is assuming things, sort of)
    qs = dict(('%s__exact' % k, v.value) for (k, v) in lookup.items())
    # Run the request!
    response = admin_client.get(reverse('admin:tests_mymodel_changelist'), data=qs)
    response.render()

    # Look for the paginator line that lists how many results we found...
    count = int(re.search('(\d+) my model', response.content.decode('utf8')).group(1))
    # and compare it to what we expect.
    assert count == MyModel.objects.filter(**lookup).count()


def test_django_admin_lookup_value_for_integer_enum_field():
    field = EnumIntegerField(Taste)

    assert field.get_prep_value(str(Taste.BITTER)) == 3, "get_prep_value should be able to convert from strings"
