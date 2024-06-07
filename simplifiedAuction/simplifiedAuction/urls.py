"""
URL configuration for simplifiedAuction project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
import simplifiedAuction.views as views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home),
    path("login", views.login),
    path("register", views.register),
    path("auction/<adminid>/dashboard", views.dashboard),
    path("auction/<adminid>/createauction", views.createAuction),
    path("auction/<auctionid>/setup", views.auctionsetup),
    path("auction/<auctionid>/live", views.liveAuction),
    path("auction/<auctionid>/final", views.finalAuction),
    path("auction/<auctionid>/view", views.viewAuction),
    path("auction/<auctionid>/addteam", views.addTeam),
    path("auction/<auctionid>/addplayer", views.addPlayer)  ,
    path("<adminid>/myauctions", views.myAuctions),
    path("allauctions", views.allAuctions),
    path("logout", views.logout),
]
