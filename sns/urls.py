"""eCast URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('signout', views.signout, name='signout'),
    path('timeline', views.timeline, name='timeline'),
    path('timeline_post', views.timeline_post, name='timeline_post'),
    path('profile_edit', views.profile_edit, name='profile_edit'),
    path('timeline_post_view', views.timeline_post_view, name='timeline_post_view'),
    path('profile_edit_view', views.profile_edit_view, name='profile_edit_view'),
    path('user_list_view', views.user_list_view, name='user_list_view'),
    path('profile', views.profile, name='profile'),
    path('other_profile', views.other_profile, name='other_profile'),
    path('timeline_api', views.timeline_api, name='timeline_api'),
    path('my_timeline_api', views.my_timeline_api, name='my_timeline_api'),
    path('user_list_api', views.user_list_api, name='user_list_api'),
    path('other_timeline_api', views.other_timeline_api, name='other_timeline_api'),
    path('user_list', views.user_list, name='user_list'),
    # path('follow_api', views.follow_api, name='follow_api'),
]
