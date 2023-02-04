from rest_framework import serializers
from backend_api.models import *
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token



class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('token', 'nombre', 'email', 'contrasena')

    def create(self, validated_data):
        user = Usuario.objects.create(**validated_data)
        return user
class PartidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partida
        fields = ('codigo', 'historia', 'createdAt', 'token_usuario')

class ParticipaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participa
        fields = ('id', 'token_usuario', 'codigo_partida')

class DibujoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dibujo
        fields = ('id', 'fecha', 'link', 'token_usuario')

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = ('id', 'comentario', 'token_usuario', 'id_dibujo')

class ValoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Valora
        fields = ('id', 'token_usuario', 'id_dibujo', 'puntuacion')