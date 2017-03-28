# -- encoding: UTF-8 --

import uuid

import pytest
from rest_framework import serializers

from enumfields.drf.serializers import EnumSupportSerializerMixin

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
    inst = MyModel(color=Color.BLUE, taste=Taste.UMAMI, int_enum=IntegerEnum.B)
    data = (LenientIntNameSerializer if int_names else MySerializer)(inst).data
    assert data['color'] == Color.BLUE.value
    if int_names:
        assert data['taste'] == 'umami'
        assert data['int_enum'] == 'b'
    else:
        assert data['taste'] == Taste.UMAMI.value
        assert data['int_enum'] == IntegerEnum.B.value


@pytest.mark.django_db
@pytest.mark.parametrize('lenient_serializer', (False, True))
@pytest.mark.parametrize('lenient_data', (False, True))
def test_deserialize(lenient_data, lenient_serializer):
    secret_uuid = str(uuid.uuid4())
    data = {
        'color': Color.BLUE.value,
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
