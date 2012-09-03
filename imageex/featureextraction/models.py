from django.db import models
import pickle

class Flower(models.Model):
    name = models.CharField(max_length=200)
    
class SampleNotExtracted(models.Model):
    flower = models.ForeignKey(Flower)
    image = models.CharField(max_length=200)
    mask = models.CharField(max_length=200)
    
class Sample(models.Model):
    flower = models.ForeignKey(Flower)
    features = models.TextField()
