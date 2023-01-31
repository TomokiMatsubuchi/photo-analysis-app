from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Photo
from photo.forms import PhotoForm, UploadImageForm
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages
from PIL import Image
import sys
import pyocr
import pyocr.builders
import xlsxwriter
import io


import pdb

# Create your views here.

class SignUpView(generic.CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy('login')
  template_name = 'photo/signup.html'

@login_required
def index(request):
  current_user = request.user
  form = UploadImageForm()
  Photos = current_user.photo_set.all()#逆参照(foreign keyが設定されていないモデルから参照)する場合,foreignkeyが設定されているモデルを小文字にして_setをつける。
  context = {
    'title': '一覧画面',
    'upload_image_form': form,
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
    form = PhotoForm(request.POST)#画像を登録するときはrequest.FILESを引数に設定する
    form.instance.author = request.user
    if form.is_valid():
      form.save()
      messages.success(request, '新規データを登録しました。')
      return redirect('index')

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
    update_form = PhotoForm(request.POST, instance=photo)
    if update_form.is_valid():
      update_form.save()
      messages.success(request, '画像を更新しました。')
      return redirect('detail', id=id)

def delete(request, id):
  photo = get_object_or_404(Photo, pk=id)
  photo.delete()
  return redirect('index')

def img_read(request):
  if request.method == 'POST':
    tools = pyocr.get_available_tools()
    img = request.FILES['image']
    #pdb.set_trace()
    image = Image.open(img)
    txt = tools[0].image_to_string(image, lang='jpn', builder=pyocr.builders.TextBuilder(tesseract_layout=6))
    initial_values = {"img_read": txt}
    form = PhotoForm(initial=initial_values)
    return render(request, 'photo/new.html', {'photoform': form})

def dl_excel(request):
  current_user = request.user
  Photos = current_user.photo_set.all()
  output = io.BytesIO()
  book = xlsxwriter.Workbook(output)
  titleformat = book.add_format({'bold': True, 'align': 'center', 'font_color': 'black', 'font_size': '14'})
  style_text = book.add_format({ 'bold': False, 'font_size': '10'})
  ws = book.add_worksheet('test')
  ws.write(0, 0, 'タイトル', titleformat)
  ws.write(0, 1, '内容', titleformat)
  ws.write(0, 2, '読み取り内容', titleformat)
  y = 1
  for photo in Photos:
    ws.write(y, 0, photo.title, style_text)
    ws.write(y, 1, photo.description, style_text)
    ws.write(y, 2, photo.img_read, style_text)
    y += 1
  book.close()
  output.seek(0)
  filename = "test.xlsx"
  response = HttpResponse(output, content_type='application/vnd.ms-excel')
  response['Content-Disposition'] = 'attachment; filename=%s' % filename
  return response

