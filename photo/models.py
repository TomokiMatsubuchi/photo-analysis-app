from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Tag(models.Model):
  name = models.CharField(max_length=30, null=False, blank=False)

  def __str__(self):
    return self.name


class Photo(models.Model):

  author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

  title = models.CharField(max_length=30, null=False, blank=False)
  description = models.TextField(null=True, blank=True)
  img_read = models.TextField(null=False, blank=False)
  created_at = models.DateTimeField(auto_now_add=True)
  tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

  def __str__(self):
    return self.title
