from django.urls import path
from . import views

app_name = 'task-manager'

urlpatterns = [
    path('', views.index, name='index'), 
    path('filtre-drh/<str:employe>', views.employe_drh, name='employe_drh'),
    path('ajouter-employe/', views.ajout_employe, name='ajout_employe'),
    path('ajouter-employe/<str:lien_a_effacer>', views.effacer_lien, name='lien_effacer'),
    path('modif-employe/<int:id_employe>', views.modif_employe, name='modif_employe'),
    path('employe-page/<int:id_employe>', views.page_employe, name='page_employe'),
    
    path('modif-info-employe/<int:id_employe>', views.modif_info_chef, name='modif_info_employe'),
]

