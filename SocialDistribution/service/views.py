from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import AuthorSerializer
from authors.models import single_author

#Display all authors in the api views
#localhost:8000/authors
@api_view(['GET'])
def authorsList(request):
    authors = single_author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data)

@api_view(['GET','POST'])
def singleAuthor(request,pk):

    if request.method == 'GET':
        author = single_author.objects.get(id = pk)
        serializer = AuthorSerializer(author, many=False)

    elif request.method == 'POST':
        author = single_author.objects.get(id = pk)
        serializer = AuthorSerializer(instance = author, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

    return Response(serializer.data)

