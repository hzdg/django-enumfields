# -- encoding: UTF-8 --
from __future__ import unicode_literals

import pytest
import six
from django.core.exceptions import ValidationError
from django.forms import BaseForm

from enumfields import EnumField

from .enums import Color, IntegerEnum


def test_choice_ordering():
    EXPECTED_CHOICES = (
        ('r', 'Reddish'),
        ('g', 'Green'),
        ('b', 'bluë'),
    )
    for ((ex_key, ex_val), (key, val)) in zip(EXPECTED_CHOICES, Color.choices()):
        assert key == ex_key
        assert six.text_type(val) == six.text_type(ex_val)


def test_custom_labels():
    # Custom label
    assert Color.RED.label == 'Reddish'
    assert six.text_type(Color.RED) == 'Reddish'
    assert six.text_type(IntegerEnum.A) == 'foo'


def test_automatic_labels():
    # Automatic label
    assert Color.GREEN.label == 'Green'
    assert six.text_type(Color.GREEN) == 'Green'
    assert six.text_type(IntegerEnum.B) == 'B'


def test_lazy_labels():
    # Lazy label
    assert isinstance(six.text_type(Color.BLUE), six.string_types)
    assert six.text_type(Color.BLUE) == 'bluë'


def test_formfield_labels():
    # Formfield choice label
    form_field = EnumField(Color).formfield()
    expectations = dict((val.value, six.text_type(val)) for val in Color)
    for value, text in form_field.choices:
        if value:
            assert text == expectations[value]


def test_formfield_functionality():
    form_cls = type(str("FauxForm"), (BaseForm,), {
        "base_fields": {"color": EnumField(Color).formfield()}
    })
    form = form_cls(data={"color": "r"})
    assert not form.errors
    assert form.cleaned_data["color"] == Color.RED


def test_invalid_to_python_fails():
    with pytest.raises(ValidationError) as ve:
        EnumField(Color).to_python("invalid")
    assert ve.value.code == "invalid_enum_value"


def test_import_by_string():
    assert EnumField("tests.test_enums.Color").enum == Color
