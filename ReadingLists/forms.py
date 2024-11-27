from django import forms

from ReadingLists.models import ReadingList


class ReadingListForm(forms.ModelForm):
    class Meta:
        model = ReadingList
        fields = ['name', 'description']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields.pop('books', None)
