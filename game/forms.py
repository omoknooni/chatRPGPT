from django import forms
from .models import Theme

class ThemeSelectionForm(forms.Form):
    theme = forms.ChoiceField(choices=[], widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super(ThemeSelectionForm, self).__init__(*args, **kwargs)
        themes = Theme.objects.order_by('?')[:4]
        self.fields['theme'].choices = [(theme.name, theme.name) for theme in themes]
