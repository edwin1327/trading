from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class role(models.Model):
    name_role = models.CharField(max_length=20, unique=True, null=False, blank=False)
    description = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name_role



class User(AbstractUser):
    picture = models.ImageField(default='userDefault.png', upload_to='users/')
    adress = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    id_role = models.ForeignKey(role, on_delete=models.CASCADE, default=1)
