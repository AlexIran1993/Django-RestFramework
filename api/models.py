
from pyexpat import model
from django.db import models
from django.conf import settings

class OwnerModel(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        abstract = True

# Create your models here.
class Categoria(OwnerModel):
    descripcion = models.CharField(max_length=100, help_text="Descripcion de la Categoria", unique=True)

    def __str__(self):
        return '{}'.format(self.descripcion)
    
    class Meta:
        verbose_name_plural = "Categorias"

class SubCategoria(OwnerModel):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=100, help_text="Descripcion de la Sub Categoria")

    def __str__(self):
        return '{}:{}'.format(self.categoria.descripcion,self.descripcion)
    
    class Meta:
        verbose_name_plural = "Sub Categorias"
        unique_together = ('categoria','descripcion')

class Producto(OwnerModel):
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=100, help_text="Descripcion del Producto", unique=True)
    fecha_creado = models.DateTimeField(auto_now_add=True)
    vendido = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.descripcion)
    
    class Meta:
        verbose_name_plural = "Productos"