from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
class Aliment(models.Model):
    nom = models.CharField(max_length=150)
    calorie = models.IntegerField()
    lipides = models.FloatField()
    cholestérol = models.FloatField()
    protéines = models.FloatField()
    potassium = models.FloatField()
    glucides = models.FloatField()
    image = models.FileField(upload_to="aliment/", max_length=250,default="pas_d'image_disponible.png")
    def __str__(self):
        return self.nom
    def get_absolute_url(self):
        return reverse("aliment_detail", kwargs={"pk": self.pk})
class Alimentation(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    aliment = models.ForeignKey(Aliment, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.utilisateur.username

class Profile(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    calorie = models.IntegerField()
    lipides = models.FloatField()
    cholestérol = models.FloatField()
    protéines = models.FloatField()
    potassium = models.FloatField()
    glucides = models.FloatField()
    def __str__(self):
        return self.utilisateur.username
    def get_absolute_url(self):
        return reverse("profile_alimentation.html", kwargs={"pk": self.pk})