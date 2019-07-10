from django.urls import path
from django.urls.conf import include
from blog import views

urlpatterns = [
    path('',views.post_list, name='post_list'),
]