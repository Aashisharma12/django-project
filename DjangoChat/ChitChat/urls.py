from django.urls import path
from . import views  # Make sure views is correctly imported

urlpatterns = [
    path('chat/', views.chatpage, name='chatpage'),
    path('login/', views.loginpage, name='loginpage'),
    path('logout/', views.logout_user, name='logout-user'),  # Logout user page (if applicable)
]
