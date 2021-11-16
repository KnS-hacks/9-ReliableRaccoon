"""DDN URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from .views import *

urlpatterns = [
    path('boardlist/', boardlist, name = "boardlist"),    
    path('boardwrite/', boardwrite, name = "boardwrite"),
    path('boardview/<int:board_id>/delete',boarddelete, name = "boarddelete"),
    path('boardrewrite/<int:board_id>/',boardrewrite, name = "boardrewrite"),
    path('boardview/<int:num>/', boardview, name = "boardview"),
    path('date_selecter_temp/', date_selecter_temp, name = "date_selecter_temp"),
    
]