from rest_framework.serializers import ModelSerializer
from .models import *

class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

class SharedNoteSerializer(ModelSerializer):
    class Meta:
        model = Share
        fields = '__all__'
