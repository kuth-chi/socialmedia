from django.contrib import admin
from .models import Note, Profile, UserFile, Share, Photo


# Register your models here.
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'body', 'updated', 'created')

    def user(self, obj):
        return obj.profile.user.username

    user.short_description = 'Profile'


admin.site.register(Note, NoteAdmin)
admin.site.register(Profile)
admin.site.register(UserFile)
admin.site.register(Photo)
admin.site.register(Share)
