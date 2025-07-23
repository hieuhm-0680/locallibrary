from __future__ import annotations

import datetime

from django import forms
from django.core.exceptions import ValidationError

from catalog.constants import RENEWAL_DATE_FUTURE_ERROR
from catalog.constants import RENEWAL_DATE_HELP_TEXT
from catalog.constants import RENEWAL_DATE_LABEL
from catalog.constants import RENEWAL_DATE_PAST_ERROR
from catalog.models import Author
from catalog.models import BookInstance


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        label=RENEWAL_DATE_LABEL,
        help_text=RENEWAL_DATE_HELP_TEXT,
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(RENEWAL_DATE_PAST_ERROR)

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(RENEWAL_DATE_FUTURE_ERROR)

        return data


class RenewBookModelForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': RENEWAL_DATE_LABEL}
        help_texts = {'due_back': RENEWAL_DATE_HELP_TEXT}
        widgets = {'due_back': forms.DateInput(attrs={'type': 'date'})}

    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(RENEWAL_DATE_PAST_ERROR)

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(RENEWAL_DATE_FUTURE_ERROR)

        return data


class AuthorModelForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'date_of_birth', 'date_of_death']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_death': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_date_of_death(self):
        data = self.cleaned_data.get('date_of_death')
        date_of_birth = self.cleaned_data.get('date_of_birth')

        if data and date_of_birth and data < date_of_birth:
            raise ValidationError(
                'Date of death cannot be before date of birth.',
            )

        return data
