from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.log_in, name='login'),
    path('register/', views.register, name='register'),
    path('link-register/<str:lien_a_tester>/', views.teste_link, name='teste_link'),
    path('logout/', views.logout_user, name='logout'),
    path('forbiden-auth/', views.forbiden_auth, name='forbiden_auth'),
    path('forbiden-link/', views.forbiden_link, name='forbiden_link'),
    
]