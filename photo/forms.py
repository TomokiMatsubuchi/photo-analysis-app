from django import forms
from .models import Photo

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'description', 'image']
        labels = {
          'title': 'タイトル',
          'description': '詳細',
          'image': '画像'
        }