from django import forms
from .models import Feedlist

class FeedForm(forms.ModelForm):
    class Meta:
        model = Feedlist
        fields = ['title', 'content', 'category']

    def __init__(self, *args, **kwargs):
        categories = kwargs.pop('categories', None)
        super().__init__(*args, **kwargs)
        if categories:
            self.fields['category'].queryset = categories