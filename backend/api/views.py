from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import NoteSerializer, SharedNoteSerializer
from .models import Note, Share


@api_view(['GET'])
def get_notes(request):
    user = request.user
    try:
        notes = Note.objects.filter(profile=user.profile)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)
    except Note.DoesNotExist:
        return Response('You do not have note yet')


@api_view(['GET'])
def get_notes_shared(request):
    shared = Share.objects.filter(user=request.user)
    serializer = SharedNoteSerializer(shared, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_note(request, pk):
    note = Note.objects.get(id=pk)
    serializer = NoteSerializer(note, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def create_note(request):
    data = request.data
    user = request.user

    note = Note.objects.create(
        profile=user.profile,
        body=data['body']
    )
    serializer = NoteSerializer(note, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def update_note(request, pk):
    data = request.data
    user = request.user  # Assuming the user is authenticated

    try:
        note = Note.objects.get(id=pk)

        # Check if the user has permission to update the note
        if note.profile != user.profile:
            share = Share.objects.filter(note=note, user=user).first()
            if not share or (share.can_read and not share.can_write):
                return Response({'detail': 'You do not have permission to update this note.'},
                                status=status.HTTP_403_FORBIDDEN)

        note.body = data['body']
        note.edited_by = user
        note.save()

        serializer = NoteSerializer(note, many=False)
        return Response(serializer.data)

    except Note.DoesNotExist:
        return Response({'detail': 'Note not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_note(request, pk):
    note = Note.objects.get(pk=pk)
    note.delete()
    return Response('Note was deleted')
