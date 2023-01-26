from django.shortcuts import render, redirect, get_object_or_404
from .models import Photo
from photo.forms import PhotoForm
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages
import pdb

# Create your views here.

class SignUpView(generic.CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy('login')
  template_name = 'photo/signup.html'

@login_required
def index(request):
  current_user = request.user
  Photos = current_user.photo_set.all()#逆参照(foreign keyが設定されていないモデルから参照)する場合,foreignkeyが設定されているモデルを小文字にして_setをつける。
  context = {
    'title': '一覧画面',
    'photos': Photos,
  }
  return render(request, 'photo/index.html', context)

def new(request):
  photoform = PhotoForm()
  context = {
    'title': '新規画面',
    'photoform': photoform,
  }
  return render(request, 'photo/new.html', context)

def create(request):
  if request.method == 'POST':
    form = PhotoForm(request.POST, request.FILES)#画像を登録するときはrequest.FILESを引数に設定する
    #pdb.set_trace()
    form.instance.author = request.user
    if form.is_valid():
      form.save()
      messages.success(request, '画像を登録しました。')
      return redirect('index')
    else:
      return render(request, 'photo/new.html', {'photoform': form})

def detail(request, id):
  photo = get_object_or_404(Photo, pk=id)
  context = {
    'title': '詳細画面',
    'photo': photo,
  }
  return render(request, 'photo/detail.html', context)

def edit(request, id):
  photo = get_object_or_404(Photo, pk=id)
  photoform = PhotoForm(instance=photo)
  context = {
    'title': '編集画面',
    'photo': photo,
    'photoform': photoform,
  }
  return render(request, 'photo/edit.html', context)

def update(request, id):
  if request.method == 'POST':
    photo = get_object_or_404(Photo, pk=id)
    update_form = PhotoForm(request.POST, request.FILES, instance=photo)
    if update_form.is_valid():
      update_form.save()
      messages.success(request, '画像を更新しました。')
      return redirect('detail', id=id)
    else:
      return render(request, 'photo/edit.html', {'photoform': update_form})

def delete(request, id):
  photo = get_object_or_404(Photo, pk=id)
  photo.delete()
  return redirect('index')