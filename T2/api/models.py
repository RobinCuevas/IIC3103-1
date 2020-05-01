from django.db import models

class Ingrediente(models.Model):
    #id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=60)
    descripcion = models.TextField(max_length=100)
    def __str__(self):
        return self.nombre

    def is_deletable(self):
            #referencia de codigo:https://gist.github.com/freewayz/69d1b8bcb3c225bea57bd70ee1e765f8
            # get all the related object
            for rel in self._meta.get_fields():
                try:
                    # check if there is a relationship with at least one related object
                    related = rel.related_model.objects.filter(**{rel.field.name: self})
                    if related.exists():
                        # if there is return a Tuple of flag = False the related_model object
                        return False, related
                except AttributeError:  # an attribute error for field occurs when checking for AutoField
                    pass  # just pass as we dont need to check for AutoField
            return True, None

class Hamburguesa(models.Model):
   # id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=60)
    precio = models.IntegerField()
    descripcion = models.TextField(max_length=100)
    imagen = models.URLField()
    ingredientes = models.ManyToManyField(Ingrediente)
    def __str__(self):
        return self.nombre
