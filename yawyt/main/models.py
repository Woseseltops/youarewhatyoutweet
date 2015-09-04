from django.db import models

# Create your models here.

class ClassifierSection(models.Model):
    classifier_module_name = models.CharField(max_length=200)
    classifier_class_name = models.CharField(max_length=200)
    template_name = models.CharField(max_length=200)
    position = models.IntegerField(default=0)

    def __str__(self):
        return self.template_name.capitalize();
