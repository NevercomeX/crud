from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework import viewsets, generics, status
from .models import Usuario, Partida, Participa, Dibujo, Comentario, Valora, Movie
from .serializers import UsuarioSerializer, PartidaSerializer, ParticipaSerializer, DibujoSerializer, ComentarioSerializer, ValoraSerializer, MovieSerializer
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes, api_view, permission_classes
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_201_CREATED
)

from django.utils import timezone



# Create your views here.
class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class PartidaViewSet(viewsets.ModelViewSet):
    queryset = Partida.objects.all()
    serializer_class = PartidaSerializer

class ParticipaViewSet(viewsets.ModelViewSet):
    queryset = Participa.objects.all()
    serializer_class = ParticipaSerializer

class DibujoViewSet(viewsets.ModelViewSet):
    queryset = Dibujo.objects.all()
    serializer_class = DibujoSerializer

class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

class ValoraViewSet(viewsets.ModelViewSet):
    queryset = Valora.objects.all()
    serializer_class = ValoraSerializer

# 2 5 8 11 14

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            if usuario:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_401_UNAUTHORIZED)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_201_CREATED)

@api_view(['GET'])
def game_detail(request, cod, token):
    try:
        game = Partida.objects.get(code=cod)
        players = Usuario.objects.filter(game=game)
    except Partida.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.session.get('token') != token:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    serializer = PartidaSerializer(game)
    serializer.data['players'] = [player.name for player in players]
    return Response(serializer.data, status=status.HTTP_200_OK)

class GetDrawingView(generics.RetrieveAPIView):
    def retrieve(self, request, cod, name, *args, **kwargs):
        # Check if the session token is valid
        if not request.session.get('token'):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # Check if the game with the provided code exists
        try:
            game = Partida.objects.get(cod=cod)
        except Partida.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Get the player with the provided name and check if it's in the game
        try:
            player = Usuario.objects.get(name=name, game=game)
        except Usuario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Get the player's drawing
        drawing = player.drawing

        return Response({
            'path': drawing.path
        })

class ShareDrawingView(generics.CreateAPIView):
    queryset = Dibujo.objects.all()
    serializer_class = DibujoSerializer

    def post(self, request, cod, format=None):
        # Check if game exists
        game = Partida.objects.filter(code=cod).first()
        if not game:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # Check if session token is valid
        if not request.session.get('token'):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        # Create and save the drawing
        drawing = Dibujo(game=game, path=request.data['path'], upload_at=timezone.now())
        drawing.save()
        serializer = DibujoSerializer(drawing)
        
        # Return success response with drawing information
        return Response(serializer.data, status=status.HTTP_200_OK)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UserViewSet(viewsets.ViewSet):
    def retrieve(self, request, name=None):
        user = Usuario.objects.get(name=name)
        drawings = Dibujo.objects.filter(user=user)
        user_serializer = UsuarioSerializer(user)
        drawings_serializer = DibujoSerializer(drawings, many=True)
        return Response({
            "user": user_serializer.data,
            "drawings": drawings_serializer.data
        })