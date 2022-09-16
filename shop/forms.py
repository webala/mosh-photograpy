from django import forms
from shop.models import Client, Shoot


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