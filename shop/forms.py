from builtins import print
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

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone[0] == '0':
            phone = '254' + phone[1:]
        elif phone[0] == '+':
            phone = phone[1:]
        elif phone[0] == '7':
            phone = '254' + phone
        
        return phone

class ShootForm(forms.ModelForm):
    class Meta:
        model = Shoot
        fields = ['date', 'location']
    
    def clean_date(self):
        date = self.cleaned_data['date']
        print(date)

        today = date.today()
        print('today: ', date > today)
        shoot = Shoot.objects.filter(date=date).first()
        if date <= today:
            print('invalid date')
            raise ValidationError('Sorry, this date is unavailable')
        elif shoot:
            print('shoot exists')
            raise ValidationError('Sorry, this date is unvailable')

        return date
