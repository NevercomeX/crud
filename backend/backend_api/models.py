from django.db import models

# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=250)
    genre = models.CharField(max_length=200)
    starring = models.CharField(max_length=350)

class Usuario(models.Model):
    token = models.CharField(max_length=256, primary_key=True)
    nombre = models.CharField(max_length=20)
    email = models.CharField(max_length=50, null=True)
    contrasena = models.CharField(max_length=20, null=True)

class Partida(models.Model):
    codigo = models.PositiveIntegerField(primary_key=True)
    historia = models.TextField(max_length=500)
    createdAt = models.DateField()
    token_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='partidas')

class Participa(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    token_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='participaciones')
    codigo_partida = models.ForeignKey(Partida, on_delete=models.CASCADE, related_name='participantes')

class Dibujo(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    fecha = models.DateField(null=True)
    link = models.URLField()
    token_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='dibujos')

class Comentario(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    comentario = models.TextField(max_length=1000)
    token_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='comentarios')
    id_dibujo = models.ForeignKey(Dibujo, on_delete=models.CASCADE, related_name='comentarios')

class Valora(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    token_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='valoraciones')
    id_dibujo = models.ForeignKey(Dibujo, on_delete=models.CASCADE, related_name='valoraciones')
    puntuacion = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name