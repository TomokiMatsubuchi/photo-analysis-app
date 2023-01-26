from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Photo(models.Model):

  author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

  image = models.ImageField(upload_to='photos/', null=False, blank=False)
  title = models.CharField(max_length=30, null=False, blank=False)
  description = models.TextField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title