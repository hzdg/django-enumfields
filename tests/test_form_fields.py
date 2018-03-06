# -- encoding: UTF-8 --
import django
import pytest
from django.utils import six
from django.db.models import BLANK_CHOICE_DASH
from django.forms.models import modelform_factory, model_to_dict

from .enums import Color, ZeroEnum
from .models import MyModel


def get_form(**kwargs):
    instance = MyModel(color=Color.RED)
    FormClass = modelform_factory(MyModel, fields=("color", "zero2", "int_enum"))
    return FormClass(instance=instance, **kwargs)


@pytest.mark.django_db
def test_unbound_form_with_instance():
    form = get_form()
    if django.VERSION >= (1, 11):
        assert 'value="r" selected' in six.text_type(form["color"])
    else:
        assert 'value="r" selected="selected"' in six.text_type(form["color"])


@pytest.mark.django_db
def test_bound_form_with_instance():
    form = get_form(data={"color": "g"})
    if django.VERSION >= (1, 11):
        assert 'value="g" selected' in six.text_type(form["color"])
    else:
        assert 'value="g" selected="selected"' in six.text_type(form["color"])


def test_choices():
    form = get_form()
    assert form.base_fields["zero2"].choices == [(0, 'Zero'), (1, 'One')]
    assert form.base_fields["int_enum"].choices == BLANK_CHOICE_DASH + [(0, 'foo'), (1, 'B')]


def test_validation():
    form = get_form(data={"color": Color.GREEN, "zero2": ZeroEnum.ZERO})
    assert form.is_valid(), form.errors

    instance = MyModel(color=Color.RED, zero2=ZeroEnum.ZERO)
    data = model_to_dict(instance, fields=("color", "zero2", "int_enum"))
    form = get_form(data=data)
    assert form.is_valid(), form.errors
