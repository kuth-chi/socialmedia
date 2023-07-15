from django.db import models


# Create your models here.
class Note(models.Model):
    body = models.TextField(verbose_name="Body")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated")
    created = models.DateTimeField(auto_now=True, verbose_name="Created")

    def __str__(self):
        return self.body[0:50]

    class Meta:
        ordering = ['-updated']
