from django.db import models

# Create your models here.

class ClassifierSection(models.Model):
    classifier_name = models.CharField(max_length=200)
    template_name = models.CharField(max_length=200)

    def __str__(self):
        return self.template_name.capitalize();
