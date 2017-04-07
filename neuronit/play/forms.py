from django import forms
from django.forms.widgets import Input

# depreciated?


class RangeInput(Input):
    """HTML5 Range Input."""
    input_type = 'range'


class RangeWidget(forms.TextInput):
    def __init__(self, min_value, max_value, attrs=None):
        super(RangeWidget, self).__init__(attrs)
        self.min_value = min_value
        self.max_value = max_value

    def render(self, name, value, attrs=None):
        attrs = attrs or {}
        value = value or [self.min_value, self.min_value]
        attrs["data-slider-value"] = str(value)
        return super(RangeWidget, self).render(name, value, attrs)


class RangeField(forms.MultiValueField):
    default_error_messages = {}
    default_min = 0
    default_max = 10

    def __init__(self, field_class, widget=forms.TextInput, min_value=None, max_value=None, *args, **kwargs):
        self.min_value = min_value or self.default_min
        self.max_value = max_value or self.default_max
        self.fields = (field_class(), field_class())

        if not 'initial' in kwargs:
            kwargs['initial'] = [self.min_value, self.min_value]

        super(RangeField, self).__init__(
            fields=self.fields, widget=RangeWidget(self.min_value, self.max_value), *args, **kwargs
        )

    def compress(self, data_list):
        if data_list:
            return [
                self.fields[0].clean(data_list[0]),
                self.fields[1].clean(data_list[1])
            ]
        return None


class GlobalParametersForm(forms.Form):
    epochs= forms.IntegerField(min_value=1,label="Number of epochs", max_value=1000, required=False,help_text="number of games you are going to play")

    simulations= forms.IntegerField(min_value=1,label="Number of simulations",required=False,help_text="number of parallel games you are going to play")
