from django.urls import path
from Center import views

urlpatterns = [
     path('auth/signup/', views.SignUp),
    path('auth/login/', views.Login),
    path('auth/me/', views.MyProfile),
    path('auth/logout/', views.Logout),
]
