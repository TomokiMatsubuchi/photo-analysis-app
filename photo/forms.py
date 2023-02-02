from django import forms
from .models import Photo

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'description', 'img_read', 'tag']
        labels = {
          'title': 'タイトル',
          'description': '詳細',
          'img_read': '画像読み取り結果',
          'tag': 'タグ'
        }

class UploadImageForm(forms.Form):
  image = forms.FileField(
    label='読み取る画像',
    required=True,
  )