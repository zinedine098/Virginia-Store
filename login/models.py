from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    STATUS_CHOICES = [
        ('kasir', 'Kasir'),
        ('admin', 'Admin'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    slogan = models.TextField(blank=True)
    alamat = models.CharField(max_length=255)
    no_telephon = models.CharField(max_length=20)
    foto_profile = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return self.nama
