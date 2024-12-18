from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token






class YourModel(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Randonnee(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_debut = models.DateTimeField(auto_now_add=True)
    distance = models.FloatField(default=0)

    def __str__(self):
        return self.titre

class Point(models.Model):
    randonnee = models.ForeignKey(Randonnee, related_name='points', on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Photo(models.Model):
    randonnee = models.ForeignKey(Randonnee, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/')
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

