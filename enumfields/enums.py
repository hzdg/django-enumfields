import inspect
from django.utils.encoding import python_2_unicode_compatible, force_bytes
from enum import Enum as BaseEnum, EnumMeta as BaseEnumMeta
import six


class EnumMeta(BaseEnumMeta):
    def __new__(cls, name, bases, attrs):
        Labels = attrs.get('Labels')

        if Labels is not None and inspect.isclass(Labels):
            del attrs['Labels']

        obj = BaseEnumMeta.__new__(cls, name, bases, attrs)
        for m in obj:
            try:
                m.label = getattr(Labels, m.name)
            except AttributeError:
                m.label = m.name.replace('_', ' ').title()

        return obj

@python_2_unicode_compatible
class Enum(six.with_metaclass(EnumMeta, BaseEnum)):
    @classmethod
    def choices(cls):
        """
        Returns a list formatted for use as field choices.
        (See https://docs.djangoproject.com/en/dev/ref/models/fields/#choices)
        """
        return tuple((m.value, m.label) for m in cls)

    def __str__(self):
        """
        Show our label when Django uses the Enum for displaying in an error message
        """
        return force_bytes(self.label)

