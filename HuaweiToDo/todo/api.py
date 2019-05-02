from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
from todo.models import Todo

from todo.serializers import TodoSerializer


@login_required
@api_view(['POST'])
def create_todo(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            serializer = TodoSerializer(data={"user": username, "text": request.data["text"]})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['GET'])
def export(request):
        if request.method == 'GET':
            models = list(Todo.objects.all())
            result = pd.DataFrame(data={
                "User": [todo.user for todo in models],
                "Todo": [todo.text for todo in models],
                "Status": [todo.is_completed for todo in models],
                "Created": [todo.created_time for todo in models],
                "Updated": [todo.last_updated for todo in models]
            })

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=filename.csv'
            result.to_csv(path_or_buf=response, sep=';', float_format='%.2f', index=False, decimal=",")
            return response

@login_required
@api_view(['GET'])
def change_status(request):

    if request.method == 'GET':
        id = request.GET.get('id', '')
        obj = Todo.objects.get(pk=id)
        if request.user.is_authenticated:
            username = request.user.username
            if obj.user == username:
                obj.is_completed = not obj.is_completed
                obj.last_updated = datetime.now()
                obj.save()
                serializer = TodoSerializer(obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@login_required
@api_view(['GET'])
def delete(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            username = request.user.username
            id = request.GET.get('id', '')
            obj = Todo.objects.get(pk=id)
            if obj.user == username:
                serializer = TodoSerializer(obj)
                obj.delete()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@login_required
@api_view(['POST'])
def import_csv(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            csv = pd.read_csv(request.FILES["csvFile"], sep=";")
            csv['Status'] = pd.np.where(csv['Status'].str.lower() == "Completed".lower(), True, False)
            csv.rename(columns={"Todo": "text", "Status": "is_completed"}, inplace=True)
            data = csv.to_dict(orient='records')
            for item in data:
                item.update({"user": username})
            serializer = TodoSerializer(data=data, many=True)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@login_required
@api_view(['GET'])
def get_statistics(request):
    models = list(Todo.objects.all())
    completed_count = 0
    not_completed_count = 0
    for i in models:
        if i.is_completed == True:
            completed_count = completed_count + 1
        else:
            not_completed_count = not_completed_count + 1
    data = [
        {"Status": "Completed", "Count": completed_count},
        {"Status": "Not Completed", "Count": not_completed_count}]
    return Response(data, status=status.HTTP_200_OK)