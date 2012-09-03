from django.db import models
from scikits.learn import svm, mixture
from imageex.util.stringutil import serialize, deserialize

# Create your models here.

class Classifier(models.Model):
    name = models.CharField(max_length=200)
    serialized = models.TextField()
    
    def setData(self, clf):
        self.serialized = serialize(clf)
    
    def getData(self):
        return deserialize(self.serialized)
