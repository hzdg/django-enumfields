from enumfields import EnumField
from django.db import models
from tests.enums import LabeledEnum


def test_shortness_check():
    class TestModel(models.Model):
        f = EnumField(LabeledEnum, max_length=3, blank=True, null=True)
        f2 = EnumField(LabeledEnum, blank=True, null=True)
    assert any([m.id == 'enumfields.max_length_fit' for m in TestModel.check()])
