import uuid

import pytest
from enumfields.drf import EnumField
from enumfields.drf.serializers import EnumSupportSerializerMixin
from rest_framework import serializers

from .enums import Color, IntegerEnum, Taste
from .models import MyModel


class MySerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'


class LenientIntNameSerializer(MySerializer):
    enumfield_options = {
        'lenient': True,
        'ints_as_names': True,
    }


@pytest.mark.parametrize('int_names', (False, True))
def test_serialize(int_names):
    inst = MyModel(
        color=Color.BLUE,
        color_not_editable=Color.BLUE,
        taste=Taste.UMAMI,
        taste_not_editable=Taste.UMAMI,
        int_enum=IntegerEnum.B,
        int_enum_not_editable=IntegerEnum.B
    )
    data = (LenientIntNameSerializer if int_names else MySerializer)(inst).data
    assert data['color'] == data['color_not_editable'] == Color.BLUE.value
    assert Color.BLUE.value
    if int_names:
        assert data['taste'] == data['taste_not_editable'] == 'umami'
        assert data['int_enum'] == data['int_enum_not_editable'] == 'b'
    else:
        assert data['taste'] == data['taste_not_editable'] == Taste.UMAMI.value
        assert data['int_enum'] == data['int_enum_not_editable'] == IntegerEnum.B.value


@pytest.mark.parametrize('instance, representation', [
    ('', ''),
    (None, None),
    ('r', 'r'),
    ('g', 'g'),
    ('b', 'b'),
])
def test_enumfield_to_representation(instance, representation):
    assert EnumField(Color).to_representation(instance) == representation


def test_invalid_enumfield_to_representation():
    with pytest.raises(ValueError, match=r"Invalid value.*"):
        assert EnumField(Color).to_representation('INVALID_ENUM_STRING')


@pytest.mark.django_db
@pytest.mark.parametrize('lenient_serializer', (False, True))
@pytest.mark.parametrize('lenient_data', (False, True))
def test_deserialize(lenient_data, lenient_serializer):
    secret_uuid = str(uuid.uuid4())
    data = {
        'color': Color.BLUE,
        'taste': Taste.UMAMI.value,
        'int_enum': IntegerEnum.B.value,
        'random_code': secret_uuid,
    }
    if lenient_data:
        data.update({
            'color': 'b',
            'taste': 'Umami',
            'int_enum': 'B',
        })
    serializer_cls = (LenientIntNameSerializer if lenient_serializer else MySerializer)
    serializer = serializer_cls(data=data)
    if lenient_data and not lenient_serializer:
        assert not serializer.is_valid()
        return
    assert serializer.is_valid(), serializer.errors

    validated_data = serializer.validated_data
    assert validated_data['color'] == Color.BLUE
    assert validated_data['taste'] == Taste.UMAMI
    assert validated_data['int_enum'] == IntegerEnum.B

    inst = serializer.save()
    assert inst.color == Color.BLUE
    assert inst.taste == Taste.UMAMI
    assert inst.int_enum == IntegerEnum.B

    inst = MyModel.objects.get(random_code=secret_uuid)  # will raise if fails
    assert inst.color == Color.BLUE
    assert inst.taste == Taste.UMAMI
    assert inst.int_enum == IntegerEnum.B
