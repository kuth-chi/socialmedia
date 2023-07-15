from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response



@api_view(["GET"])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/notes',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of notes'
        },
        {
            'Endpoint': '/notes/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single note object'
        },
        {
            'Endpoint': '/notes/create',
            'method': 'POST',
            'body': {"body": " "},
            'description': 'Create a note with data form'
        },
        {
            'Endpoint': '/notes/id/update',
            'method': 'PUT',
            'body': {"body": " "},
            'description': 'Create an existing note with data'
        },
        {
            'Endpoint': '/notes/id/delete',
            'method': 'delete',
            'body': None,
            'description': 'Delete an existing note'
        },
    ]
    return Response(routes)
