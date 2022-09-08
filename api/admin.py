from django.contrib import admin
from .models import Producto, Categoria, SubCategoria

# Register your models here.
admin.site.register(Categoria)
admin.site.register(SubCategoria)