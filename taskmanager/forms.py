from django import forms
from .models import LienConnexion
from django.utils.translation import gettext_lazy as _


class LienConnexionForm(forms.ModelForm):
    
    class Meta:
        model = LienConnexion
        fields = ('role_lien', 'poste_lien')
        widgets = {
            'poste_lien': forms.TextInput(attrs={
                'class': 'field_input'
            })
        }
        
class ModificationEmploye(forms.Form):
    role_employe = forms.ChoiceField(label="Le rôle de l'employé", choices=[])
    poste_employe = forms.CharField(
        label="Poste employé", 
        max_length=100, 
        required=True, 
        widget= forms.TextInput(attrs={'class':'field_input'}) 
    )
    
    def __init__(self, *args, **kwargs) :
        super(ModificationEmploye, self).__init__(*args, **kwargs)
        self.fields['role_employe'].choices = [ (role[0], role[1]) for role in LienConnexion.ROLE_CHOICES ]