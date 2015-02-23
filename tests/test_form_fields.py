# -- encoding: UTF-8 --

from django.forms.models import modelform_factory
import pytest
from .models import MyModel
import six


def get_form(**kwargs):
    instance = MyModel(color=MyModel.Color.RED)
    FormClass = modelform_factory(MyModel, fields=("color",))
    return FormClass(instance=instance, **kwargs)


@pytest.mark.django_db
def test_unbound_form_with_instance():
    form = get_form()
    assert 'value="r" selected="selected"' in six.text_type(form["color"])


@pytest.mark.django_db
def test_bound_form_with_instance():
    form = get_form(data={"color": "g"})
    assert 'value="g" selected="selected"' in six.text_type(form["color"])
