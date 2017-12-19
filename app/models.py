from django.contrib.auth.models import User
from django.db import models


class Contact(models.Model):
    owner = models.ForeignKey(to=User, related_name='owner',on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    phone = models.CharField(max_length=11)
    qq = models.CharField(max_length=15)
    wechat = models.CharField(max_length=50)
    email = models.EmailField()

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name