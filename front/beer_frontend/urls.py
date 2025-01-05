"""
URL configuration for beer_frontend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from . import views

urlpatterns = [
    path("", views.recommend_beer, name="recommend_beer"),
    path("add_beer/", views.add_beer, name="add_beer"),
    path("recommend/", views.recommend_page, name="recommend_page"),
    path("add_beer_page/", views.add_beer_page, name="add_beer_page"),  # Новый маршрут
]
