from dataclasses import field, fields
from pyexpat import model
from rest_framework import serializers
from .models import Categoria, Producto, SubCategoria
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

#Clase que serializara un formulario del modelo Producto
class ProductoSerializer(serializers.ModelSerializer):

    owner = serializers.HiddenField(
        #Obtencion del usuario logiado
        default = serializers.CurrentUserDefault()
    )

    class Meta:
        model = Producto
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):

    owner = serializers.HiddenField(
        #Obtencion del usuario logiado
        default = serializers.CurrentUserDefault()
    )

    class Meta:
        model = Categoria
        fields = '__all__'

class SubCategoriaSerializer(serializers.ModelSerializer):

    owner = serializers.HiddenField(
        #Obtencion del usuario logiado
        default = serializers.CurrentUserDefault()
    )

    class Meta:
        model = SubCategoria
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #Solo se usaran tres campos del modelo User
        fields = ('username','email','password')
        #El campo password solo sera de escritura.
        extra_kwargs = {'password':{'write_only':True}}
    
    #Creacion del objeto user con la data del nuevo usuario
    def create(self, validated_data):
        user = User(
            email = validated_data['email'],
            username = validated_data['username']
        )
        #Validacion del password para el usuario creado
        user.set_password(validated_data['password'])
        #Guardado del regitro en el modelo User
        user.save()
        #Creacion del token
        Token.objects.create(user=user)
        #Retorno del objeto user
        return user

