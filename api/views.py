#from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
#from django.shortcuts import get_object_or_404

from rest_framework import generics

from rest_framework import viewsets

from .models import Categoria, Producto, SubCategoria
from . import serializer

from .permissions import IsOwner
from rest_framework.permissions import IsAuthenticated

# Create your views here.
#class PrductoList(APIView):
#    def get(self, request):
#        prod = Producto.objects.all()[:20]
#        data = ProductoSerializer(prod, many=True).data
#        return Response(data)

#class ProductoDetalle(APIView):
#    def get(self, request, pk):
#        prod = get_object_or_404(Producto, id=pk)
#        data = ProductoSerializer(prod).data
#        return Response(data)

#Simplificando las vistas

class ProductoList(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = serializer.ProductoSerializer

class ProductoDetalle(generics.RetrieveDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = serializer.ProductoSerializer


#class CategoriaSave(generics.CreateAPIView):
#    serializer_class = serializer.CategoriaSerializer

class CategoriaList(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = serializer.CategoriaSerializer

#class SubCategoriaSave(generics.CreateAPIView):
#    serializer_class = serializer.SubCategoriaSerializer

class SubCategoriaListAll(generics.ListCreateAPIView):
    queryset = SubCategoria.objects.all()
    serializer_class = serializer.CategoriaSerializer

class CategoriaDetalle(generics.RetrieveDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = serializer.CategoriaSerializer

#Extraccion del pk de la subcategoria la cual se encuentra en la url para buscar el registro compatible
class SubCategoriaList(generics.ListCreateAPIView):
    def get_queryset(self):
        #Se traen los registros de SubCategoria que correspondad a el pk de la url con la propiedad categoria_id del modelo SubCategoria
        queryset = SubCategoria.objects.filter(categoria_id=self.kwargs["pk"])
        return queryset
    serializer_class = serializer.SubCategoriaSerializer

#Clase diferente usado para añadir data a la base de datos
class SubCategoriaAdd(APIView):
    #Meodo post para añadir un registro a SubCategoria
    def post (self, request, cat_pk):
        #Extraccion del valor descripcion desde el request
        descripcion = request.data.get("descripcion")
        #Creacion del objeto Json con categoria y descripcion
        data = {
            'categoria': cat_pk,
            'descripcion': descripcion
        }
        #Serializacion del objeto Json con SubCategoriaSerializer
        serializerobj = serializer.SubCategoriaSerializer(data=data)
        #Validacin de la serializacion de data
        if serializerobj.is_valid():
            #En caso de que la serializacion sea valida, se hace el registro en la base de datos
            subcat = serializerobj.save()
            #Retorno del objeto data serializado el status 201
            return Response(serializerobj.data, status = status.HTTP_201_CREATED)
        #En caso de que no sea valido se reornan los errores y el status en 400
        else:
            return Response(serializerobj.errors, status = status.HTTP_400_BAD_REQUEST)

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = serializer.ProductoSerializer
    #Modificacion de los permisos usando la clase IsOwner como validador por default.
    permission_classes =([
        #Permiso con propierar para evalaurlo en Postman
        IsAuthenticated,
        #Permiso creado en el archvio permissions.py
        IsOwner
    ])

class UserCreate(generics.CreateAPIView):
    #Se deja las propiedades de autenticacion vacias para tomar por default las de res_framework
    authentication_classes = ()
    permission_classes = ()
    serializer_class = serializer.UserSerializer

class LoginView(APIView):
    #Especificacion que no se usara ningun permiso de clase
    permission_classes = ()

    #Si el request ejecutado es un POST de ejecutara este metodo
    def post(self, request):
        #Se extrae los valores de username y password del request y se alamcenan en variables diferenetes
        username = request.data.get("username")
        password = request.data.get("password")
        #Autenticacion del usuario usando los valores de username y password
        user = authenticate(username=username,password=password)
        #Si el usuario autenticado es verdadero se extrae el valor de la propiedad token y se envia como respuesta
        if user:
            return Response({"token": user.auth_token.key})
        #En caso de que el objeto user sea falso se retorna el error de autenticacion y el estado en 400
        else:
            return Response({"error": "Credenciales Incorrectas"}, status=status.HTTP_400_BAD_REQUEST)