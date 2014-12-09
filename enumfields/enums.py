import inspect
from django.utils.encoding import python_2_unicode_compatible
from enum import Enum as BaseEnum, EnumMeta as BaseEnumMeta, _EnumDict

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text


class EnumMeta(BaseEnumMeta):
    def __new__(mcs, name, bases, attrs):
        Labels = attrs.get('Labels')

        if Labels is not None and inspect.isclass(Labels):
            del attrs['Labels']
            if hasattr(attrs, '_member_names'):
                attrs._member_names.remove('Labels')

        obj = BaseEnumMeta.__new__(mcs, name, bases, attrs)
        for m in obj:
            try:
                m.label = getattr(Labels, m.name)
            except AttributeError:
                m.label = m.name.replace('_', ' ').title()

        return obj


@python_2_unicode_compatible
class Enum(EnumMeta('Enum', (BaseEnum,), _EnumDict())):
    @classmethod
    def choices(cls):
        """
        Returns a list formatted for use as field choices.
        (See https://docs.djangoproject.com/en/dev/ref/models/fields/#choices)
        """
        return tuple((m.value, m.label) for m in cls)

    def __str__(self):
        """
        Show our label when Django uses the Enum for displaying in a view
        """
        return force_text(self.label)
