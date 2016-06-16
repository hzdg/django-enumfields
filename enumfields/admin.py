from django.contrib.admin.options import IncorrectLookupParameters
from django.contrib.admin import FieldListFilter


class EnumFieldListFilter(FieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        try:
            self.lookup_val = field.enum(request.GET[self.field_path])
        except KeyError:
            self.lookup_val = None
        except ValueError as e:
            raise IncorrectLookupParameters(e)

    def expected_parameters(self):
        return [self.field_path]

    def choices(self, changelist):
        yield {
            'selected': self.lookup_val is None,
            'query_string': changelist.get_query_string({}, [self.field_path]),
            'display': 'All'
        }
        for value in self.field.enum:
            yield {
                'selected': value == self.lookup_val,
                'query_string': changelist.get_query_string({self.field_path: value.value}),
                'display': value.label,
            }

    def queryset(self, request, queryset):
        if self.lookup_val is not None:
            queryset = queryset.filter(**{
                self.field_path: self.lookup_val,
            })
        return queryset
