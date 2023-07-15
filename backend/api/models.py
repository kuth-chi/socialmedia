import os

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _
from django.core.files import File


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(blank=True, verbose_name=_('date of birth'))


class Photo(models.Model):
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    image_title = models.CharField(max_length=100, blank=True, verbose_name=_('image title'))
    image_caption = models.CharField(max_length=250, blank=True, verbose_name=_('Image Caption'))
    image = models.ImageField(upload_to="profile/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Note(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='notes', verbose_name="User ID", blank=True, null=True)
    body = models.TextField(verbose_name="Body")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated")
    created = models.DateTimeField(auto_now=True, verbose_name="Created")

    def __str__(self):
        return self.body[0:50]

    class Meta:
        ordering = ['-updated']


class UserFile(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='files', blank=True, null=True)
    file = models.FileField(upload_to='note/files/')
    file_name = models.CharField(max_length=250, blank=True)
    file_size = models.CharField(max_length=20, blank=True)
    file_type = models.CharField(max_length=50, blank=True)

    def save(self, *args, **kwargs):
        if self.file:
            self.file_name = self.file.name
            self.file_type = self.file.content_type
            self.file_size = self.calculate_file_size()

        super().save(*args, **kwargs)

    def calculate_file_type(self):
        file_name = self.file.name
        _, extension = os.path.splitext(file_name)
        return extension

    def calculate_file_size(self):
        size = self.file.size
        kb_size = size / 1024
        if kb_size < 1024:
            return f"{kb_size:.2f} KB"
        elif kb_size < 1024 ** 2:
            return f"{kb_size / 1024:.2f} MB"
        else:
            return f"{kb_size / (1024 ** 2):.2f} GB"

    @property
    def file_obj(self):
        if self.pk and self.file_name:
            try:
                return File(open(self.file_name, 'rb'))
            except FileNotFoundError:
                return None

        return None


# Sharing the notes
class Share(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    can_read = models.BooleanField(default=False)
    can_write = models.BooleanField(default=False)
