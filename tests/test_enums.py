from django.core.exceptions import ValidationError
from django.forms import BaseForm

import pytest
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
        assert str(val) == str(ex_val)


def test_custom_labels():
    # Custom label
    assert Color.RED.label == 'Reddish'
    assert str(Color.RED) == 'Reddish'
    assert str(IntegerEnum.A) == 'foo'


def test_automatic_labels():
    # Automatic label
    assert Color.GREEN.label == 'Green'
    assert str(Color.GREEN) == 'Green'
    assert str(IntegerEnum.B) == 'B'


def test_lazy_labels():
    # Lazy label
    assert isinstance(str(Color.BLUE), str)
    assert str(Color.BLUE) == 'bluë'


def test_formfield_labels():
    # Formfield choice label
    form_field = EnumField(Color).formfield()
    expectations = {val.value: str(val) for val in Color}
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


def test_invalid_to_python_fails():
    with pytest.raises(ValidationError) as ve:
        EnumField(Color).to_python("invalid")
    assert ve.value.code == "invalid_enum_value"


def test_import_by_string():
    assert EnumField("tests.test_enums.Color").enum == Color
