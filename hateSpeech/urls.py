"""sandbox URL Configuration

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
from django.contrib import admin
from django.urls import path
from hsApp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index),
    path("sfReg", views.sfReg),
    path("login/", views.login),
    path("/", views.logout,name='logout'),
    path("adminHome", views.adminHome),
    path("sfHome", views.sfHome),
    path("sfProfile", views.sfProfile),
    path("sfChangeImage", views.sfChangeImage),
    path("sfPost", views.sfPost),
    path("sfViewSelfPost", views.sfViewSelfPost),
    path("sfUpdateIdea", views.sfUpdateIdea),
    path("sfDeleteIdea", views.sfDeleteIdea),
    path("sfViewIdea", views.sfViewIdea),
    path("sfViewSf", views.sfViewSf),
    path("sfAddFeedBack", views.sfAddFeedBack),
    path("sfChat", views.sfChat),
    path("sfChatPer", views.sfChatPer),
    path("adminStartUp", views.adminStartUp),
    path("approveStartUp", views.approveStartUp),
    path("adminViewFeedback", views.adminViewFeedback),
    path("adminViewDetections", views.adminViewDetections),
]
