# Register your models here.
from django.contrib import admin
from .models import CustomUser, Task  # Importa tus modelos

# Registra tus modelos aquí
admin.site.register(CustomUser)
admin.site.register(Task)