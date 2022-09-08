from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Categoria

# Create your views here.
def categoria_list(request):
    #Variable que representa la cantidad total de registros que se traeran de la base de datos
    MAX_OBJECTS = 20
    #Queryset a la tabla Categorias
    cat = Categoria.objects.all()[:MAX_OBJECTS]
    #Creacion del objeto Json con los resultados del Queryset
    data = {
            "results":list(cat.values("descripcion","activo"))
        }
    #Retorno del Json a travez del paquete Jsonresponse
    return JsonResponse(data)

def categoria_detalle(request, pk):
    #QuerySet a la tabla Categoria, peticion del registro igual al pk del parametro o retorno de un error 404
    cat = get_object_or_404(Categoria, id=pk)
    #Construccion del objeto Json
    data = {
        "results": {
            "descripcion": cat.descripcion,
            "activo": cat.activo
        }
    }
    #Retorno del objeto Json
    return JsonResponse(data)
