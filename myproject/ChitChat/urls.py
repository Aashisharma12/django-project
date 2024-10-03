from django.urls import path
from . import views  # Make sure views is correctly imported

urlpatterns = [
    path('', views.chatpage, name='chatpage'),  # Map root URL to chatPage view
    path('chat/', views.chatpage, name='chatpage'),
    path('login/', views.loginpage, name='loginpage'),
    path('logout/', views.logout_user, name='logout-user'),  # Logout user page (if applicable)
]
