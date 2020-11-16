from django.db.models import BLANK_CHOICE_DASH
from django.forms.models import model_to_dict, modelform_factory

import pytest

from .enums import Color, ZeroEnum
from .models import MyModel


def get_form(**kwargs):
    instance = MyModel(color=Color.RED)
    FormClass = modelform_factory(MyModel, fields=("color", "zero", "int_enum"))
    return FormClass(instance=instance, **kwargs)


@pytest.mark.django_db
def test_unbound_form_with_instance():
    form = get_form()
    assert 'value="r" selected' in str(form["color"])


@pytest.mark.django_db
def test_bound_form_with_instance():
    form = get_form(data={"color": "g"})
    assert 'value="g" selected' in str(form["color"])


@pytest.mark.django_db
def test_bound_form_with_instance_empty():
    form = get_form(data={"color": None})
    assert 'value="" selected' in str(form["color"])


def test_choices():
    form = get_form()
    assert form.base_fields["zero"].choices == [(0, 'Zero'), (1, 'One')]
    assert form.base_fields["int_enum"].choices == BLANK_CHOICE_DASH + [(0, 'foo'), (1, 'B')]


def test_validation():
    form = get_form(data={"color": Color.GREEN, "zero": ZeroEnum.ZERO})
    assert form.is_valid(), form.errors

    instance = MyModel(color=Color.RED, zero=ZeroEnum.ZERO)
    data = model_to_dict(instance, fields=("color", "zero", "int_enum"))
    form = get_form(data=data)
    assert form.is_valid(), form.errors
