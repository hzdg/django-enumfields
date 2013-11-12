Installation
------------

1. ``pip install django-enumfields``


Included Tools
--------------

Enum
````

The ``Enum`` class lets you quickly define enumeration types for model field
values. It uses `Pep 435`__-style enums, but has some extra model-specific
functionality (like the ability to easily add custom labels).


__ http://www.python.org/dev/peps/pep-0435/


Usage
'''''

In models.py:

.. code-block:: python

	from enumfields import Enum

	class MyModel(models.Model):

	    Color = Enum(
	        RED=('r', 'Red'),
	        GREEN=('g', 'Green'),
	        BLUE=('b', 'Blue'),
	    )

	    color = models.CharField(max_length=1, choices=Color.choices())

Elsewhere:

.. code-block:: python

	m = MyModel.objects.filter(color=MyModel.Color.RED)


Custom Labels
'''''''''''''

By default, labels are title-cased versions of your enum member names (e.g.
"Red" for ``Color.RED``). You can customize this with an inner ``Labels`` class.

.. code-block:: python

	class Color(Enum):
	    RED = 'r'
	    GREEN = 'g'
	    BLUE = 'b'

	    class Labels:
	        RED = 'El color del diablo'
