This package lets you use real Python (PEP435_-style) enums with Django.

.. image:: https://travis-ci.org/hzdg/django-enumfields.svg?branch=master
    :target: https://travis-ci.org/hzdg/django-enumfields


Installation
------------

1. ``pip install django-enumfields``


Included Tools
--------------


EnumField, EnumIntegerField
```````````````````````````

.. code-block:: python

    from enumfields import EnumField
    from enumfields import Enum  # Uses Ethan Furman's "enum34" backport

    class MyModel(models.Model):

        class Color(Enum):
            RED = 'r'
            GREEN = 'g'
            BLUE = 'b'

        color = EnumField(Color, max_length=1)

Elsewhere:

.. code-block:: python

    m = MyModel.objects.filter(color=MyModel.Color.RED)

``EnumIntegerField`` works identically, but the underlying storage mechanism is
an ``IntegerField`` instead of a ``CharField``.


Enum
````

Normally, you just use normal PEP435_-style enums, however, django-enumfields
also encludes its own version of Enum with a few extra bells and whistles.
Namely, the smart definition of labels which are used, for example, in admin
dropdowns. By default, it will create labels by title-casing your constant
names. You can provide custom labels with a nested "Labels" class.

.. code-block:: python

    from enumfields import EnumField, Enum  # Our own Enum class

    class MyModel(models.Model):

        class Color(Enum):
            RED = 'r'
            GREEN = 'g'
            BLUE = 'b'

            class Labels:
            	RED = 'A custom label'

        color = EnumField(Color, max_length=1)

    assert MyModel.Color.GREEN.label == 'Green'
    assert MyModel.Color.RED.label == 'A custom label'


.. _PEP435: http://www.python.org/dev/peps/pep-0435/


EnumFieldListFilter
``````````````````

``enumfields.admin.EnumFieldListFilter`` is provided to allow using enums in
``list_filter``.


.. code-block:: python

    from enumfields.admin import EnumFieldListFilter

    class MyModelAdmin(admin.ModelAdmin):
      list_filter = [('color', EnumFieldListFilter)]
