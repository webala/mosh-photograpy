from django import forms
from shop.models import Client, Shoot
from datetime import date
from django.core.exceptions import ValidationError


class ImageUploadForm(forms.Form):
    image = forms.FileField()


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'phone', 'email']

class ShootForm(forms.ModelForm):
    class Meta:
        model = Shoot
        fields = ['date', 'location']
    
    def clean_date(self):
        date = self.cleaned_data['date']
        today = date.today()
        shoot = Shoot.objects.filter(date=date).first()
        if date <= today:
            raise ValidationError('Sorry, this date is unavailable')
        elif shoot:
            raise ValidationError('Sorry, this date is unvailable')

        return date
