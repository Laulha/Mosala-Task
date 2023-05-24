import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


# Create your models here.
class LienConnexion (models.Model):
    
    CHEF = 'CHEF'
    EMPLOYE = 'EMPLOYE'
    
    ROLE_CHOICES = (
        (CHEF, 'Chef de groupe'),
        (EMPLOYE, 'Employé')
    )
    
    lien_connexion = models.CharField(_("Le lien de connexion"), max_length=60, unique=True, null=False, blank=False)
    statut_lien = models.IntegerField(_("Le statut du lien"), default=0)
    role_lien = models.CharField(_("Le role que va avoir l'employé"), max_length=10, default='EMPLOYE', choices=ROLE_CHOICES, null=False, blank=False)
    poste_lien = models.CharField(_("Post employé"), max_length=50, null=False, blank=False)
    employe = models.ForeignKey(get_user_model(), verbose_name=_("L'employé inscrit"), null=True, on_delete=models.SET_NULL, related_name='lienconnexion')
    date_creation = models.DateField(_("Date de création"), auto_now=True, auto_now_add=False)
    
    def genere_lien (self):
        return str(uuid.uuid4())[:33]