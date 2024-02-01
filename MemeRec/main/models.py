from django.db import models

# Create your models here.

class DummyModel(models.Model):
    image_name = models.CharField(max_length=100)
    user_id = models.IntegerField()
