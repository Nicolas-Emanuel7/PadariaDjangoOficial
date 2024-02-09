from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario (AbstractUser):
    telefone = models.CharField(max_length=20)
    cpf = models.CharField(max_length=11, primary_key=True, unique=True)
    endereco = models.CharField(max_length=255)
    permissao = models.BooleanField(default=False)
    groups = models.ManyToManyField('auth.Group', related_name='usuarios', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='usuarios', blank=True)

    REQUIRED_FIELDS = ['email']
    

    def __str__(self) -> str:
        return self.username

