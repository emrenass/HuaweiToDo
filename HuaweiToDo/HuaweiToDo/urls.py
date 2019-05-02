"""HuaweiToDo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from todo import views
from todo import api
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('home/', views.home, name='home'),
    path('statistics/', views.statistics, name='statistics'),

    path('api/v1/change_status', api.change_status),
    path('api/v1/create_todo', api.create_todo),
    path('api/v1/export', api.export),
    path('api/v1/delete', api.delete),
    path('api/v1/import', api.import_csv),
    path('api/v1/get_statistics', api.get_statistics),
]
