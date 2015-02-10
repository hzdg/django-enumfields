# -- encoding: UTF-8 --

from django.forms import BaseForm
from django.utils.translation import ugettext_lazy
from enumfields import Enum, EnumField
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
