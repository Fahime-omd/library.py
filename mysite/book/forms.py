from calendar import week
from django import forms
import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


#فرم تمدیدتاریخ کتاب

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a data between now and four weeks.")



#  (validation) اعتبار سنجی
def clean_renewal_date(self):
    data = self.cleaned_data['renewal_date']
    if data < datetime.date.today():
        raise ValidationError(_('Invalid date - renewal in past'))

    if data > datetime.date.today() + datetime.timedelta(weeks = 4):
        raise ValidationError(_('Invalid date - renewal more than 4 wreeks ahead.'))

    return data
