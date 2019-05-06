"""
This module contains views for RestAPI, none of these views has templates
and all of them require authentication in order to execute, they redirect to
login page otherwise.
"""


from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
from todo.models import Todo

from todo.serializers import TodoSerializer


@login_required
@api_view(['POST'])
def create_todo(request):
    """ This method create new to-do item based
    on currently logged in user and a to-do text in request
    :param request:
    :return: HTTP_201_CODE if to-do created successfully
            HTTP_400_CODE if to-do could not created successfully
    """
    if request.user.is_authenticated:
        username = request.user.username
        try:
            serializer = TodoSerializer(data={"user": username, "text": request.data["text"]})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KeyError:
            pass
    return Response(status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['GET'])
def export(request):
        """ This method export all to-do items to
        csv file which is seperated by semicolon ';'

        :param request:
        :return response: Contains csv file
        """
        models = list(Todo.objects.all())
        result = pd.DataFrame(data={
            "User": [todo.user for todo in models],
            "Todo": [todo.text for todo in models],
            "Status": [todo.is_completed for todo in models],
            "Created": [todo.created_time for todo in models],
            "Updated": [todo.last_updated for todo in models]
        })

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=todo.csv'
        result.to_csv(path_or_buf=response, sep=';', float_format='%.2f', index=False, decimal=",")
        return response

@login_required
@api_view(['GET'])
def change_status(request):
    """ This method change current status
    of to-do item. If item completed then method changes
    it to not completed, if to-do is not completed it changes
    to completed

    :param request: takes id of to-do item to change from request
    :return: Changed to-do item and HTTP_200_CODE if method executed successfully
            HTTP_400_CODE if method encountered with error.
    """
    id = request.GET.get('id', '')
    obj = Todo.objects.get(pk=id)
    if request.user.is_authenticated:
        username = request.user.username
        if obj.user == username:
            serializer = TodoSerializer(obj, data={"is_completed": not obj.is_completed,
                                                   "last_updated": timezone.now()}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['GET'])
def delete(request):
    """ This method deletes selected to-do item

    :param request: takes id of to-do item to delete from request
    :return: Deleted to-do item and HTTP_200_CODE if method executed successfully
            HTTP_400_CODE if method encountered with error.
    """
    if request.user.is_authenticated:
        username = request.user.username
        id = request.GET.get('id', '')
        obj = Todo.objects.get(pk=id)
        if obj.user == username:
            serializer = TodoSerializer(obj)
            obj.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['POST'])
def import_csv(request):
    """ This method creates to-do item
    from a csv file. Given csv should be seperated by semicolon ';'
    Csv file taken from request.FILES

    :param request:
    :return: All to-do items if they created successfully and HTTP_201_CODE
            HTTP_400_CODE if to-do  items could not created successfully
    """
    if request.user.is_authenticated:
        username = request.user.username
        file = request.FILES["csvFile"]
        if file.name.lower().endswith(".csv"):
            csv = pd.read_csv(request.FILES["csvFile"], sep=";")
            csv['Status'] = pd.np.where(csv['Status'].str.lower() == "completed", True, False)
            csv.rename(columns={"Todo": "text", "Status": "is_completed"}, inplace=True)
            data = csv.to_dict(orient='records')
            for item in data:
                item.update({"user": username})
            serializer = TodoSerializer(data=data, many=True)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['GET'])
def get_statistics(request):
    """ This method calculate total count of
    both completed and not completed items

    :param request:
    :return: Dictionary contains counts of completed and not completed item
    """
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