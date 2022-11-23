from django import forms
from .models import Request
import datetime
class RequestForm(forms.ModelForm):
    """Form enabling students to make lesson requests."""

    class Meta:
        model = Request
        fields = ['availability', 'number_of_lessons','interval_between_lessons', 'duration_of_lessons', 'instrument', 'teacher']
        widgets = {
            'availability' : forms.SplitDateTimeWidget( date_attrs={'type' : 'date', 'min': datetime.date.today() }, time_format='%H:%M:%S', time_attrs={'type' : 'time', 'min': '08:00', 'max': '17:30'} ),
            'instrument' : forms.Select(),
            'interval_between_lessons' : forms.NumberInput(),
            'number_of_lessons' : forms.NumberInput(),
            'duration_of_lessons' : forms.Select(),
        }
    # def clean(self):
    #     """Clean the data and generate messages for any errors."""

    #     super().clean()
  

    # def save(self):
    #     """Create a new request."""
    #     super().save(commit=False)
    #     request = Request.objects.create(
    #         availability=self.cleaned_data.get('availability'),
    #         number_of_lessons=self.cleaned_data.get('number_of_lessons'),
    #         interval_between_lessons = self.cleaned_data.get('interval_between_lessons'),
    #         duration_of_lessons=self.cleaned_data.get('duration_of_lessons'),
    #         instrument=self.cleaned_data.get('instrument'),
    #         teacher=self.cleaned_data.get('teacher'),
    #     )
    #     return request