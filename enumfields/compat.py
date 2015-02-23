# -- encoding: UTF-8 --
from django.forms import TypedChoiceField, CharField
from django.utils.text import capfirst

__all__ = ["formfield"]

# This is a copy of Django 1.8's (78d43a5e1064b63db1c486516c4263ef1c4c975c)
# `Field.formfield()`, for compatibility with Django 1.5.x, which does not
# support `choices_form_class` in a sane way.
# The commit b6f4a92ff45d98a63dc29402d8ad86b88e6a6697
# would make this compatible with our enums,
# but it's best to go all the way to the freshest code, I think.

def formfield(db_field, form_class=None, choices_form_class=None, **kwargs):
    """
    Returns a django.forms.Field instance for this database Field.
    """
    defaults = {'required': not db_field.blank,
                'label': capfirst(db_field.verbose_name),
                'help_text': db_field.help_text}
    if db_field.has_default():
        if callable(db_field.default):
            defaults['initial'] = db_field.default
            defaults['show_hidden_initial'] = True
        else:
            defaults['initial'] = db_field.get_default()
    if db_field.choices:
        # Fields with choices get special treatment.
        include_blank = (db_field.blank or
                         not (db_field.has_default() or 'initial' in kwargs))
        defaults['choices'] = db_field.get_choices(include_blank=include_blank)
        defaults['coerce'] = db_field.to_python
        if db_field.null:
            defaults['empty_value'] = None
        if choices_form_class is not None:
            form_class = choices_form_class
        else:
            form_class = TypedChoiceField
        # Many of the subclass-specific formfield arguments (min_value,
        # max_value) don't apply for choice fields, so be sure to only pass
        # the values that TypedChoiceField will understand.
        for k in list(kwargs):
            if k not in ('coerce', 'empty_value', 'choices', 'required',
                         'widget', 'label', 'initial', 'help_text',
                         'error_messages', 'show_hidden_initial'):
                del kwargs[k]
    defaults.update(kwargs)
    if form_class is None:
        form_class = CharField
    return form_class(**defaults)

# This is a bare-bones implementation of `import_string`, as
# implemented in Django commit f95122e541df5bebb9b5ebb6226b0013e5edc893.

try:
    try:
        from django.utils.module_loading import import_string
    except ImportError:
        from django.utils.module_loading import import_by_path as import_string
except ImportError:
    from django.utils.importlib import import_module
    def import_string(dotted_path):
        module_path, class_name = dotted_path.rsplit('.', 1)
        module = import_module(module_path)
        return getattr(module, class_name)

