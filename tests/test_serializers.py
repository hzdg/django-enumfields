# -- encoding: UTF-8 --

import uuid

import pytest
from rest_framework import serializers

from enumfields.drf.serializers import EnumSupportSerializerMixin

from .models import MyModel
from .enums import Color, IntegerEnum, Taste


class MySerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'


def test_serialize():
    inst = MyModel(color=Color.BLUE, taste=Taste.UMAMI, int_enum=IntegerEnum.B)
    data = MySerializer(inst).data
    assert data['color'] == Color.BLUE.value
    assert data['taste'] == Taste.UMAMI.value
    assert data['int_enum'] == IntegerEnum.B.value


@pytest.mark.django_db
def test_deserialize():
    secret_uuid = str(uuid.uuid4())
    data = {
        'color': Color.BLUE.value,
        'taste': Taste.UMAMI.value,
        'int_enum': IntegerEnum.B.value,
        'random_code': secret_uuid
    }
    serializer = MySerializer(data=data)
    assert serializer.is_valid()

    validated_data = serializer.validated_data
    assert validated_data['color'] == Color.BLUE
    assert validated_data['taste'] == Taste.UMAMI
    assert validated_data['int_enum'] == IntegerEnum.B

    inst = serializer.save()
    assert inst.color == Color.BLUE
    assert inst.taste == Taste.UMAMI
    assert inst.int_enum == IntegerEnum.B

    try:
        inst = MyModel.objects.get(random_code=secret_uuid)
    except DoesNotExist:
        assert False, "Object wasn't created in the database"
    assert inst.color == Color.BLUE
    assert inst.taste == Taste.UMAMI
    assert inst.int_enum == IntegerEnum.B
