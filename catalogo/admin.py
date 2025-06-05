from django.contrib import admin
from .models import EjemplarLibro, Libro, Genero, Autor

# Register your models here.

admin.site.register(EjemplarLibro)
admin.site.register(Libro)
admin.site.register(Genero)
admin.site.register(Autor)