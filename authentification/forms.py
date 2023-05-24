from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from authentification.models import MyUser
from django.core.exceptions import ValidationError


class ConnectionForm(forms.Form):
    email_or_phone = forms.CharField(
        label='Email/Tel',
        label_suffix=' **',
        help_text='Votre numéro doit commencer par 00',
        max_length=60, 
        required=True,
        widget=forms.TextInput (attrs={
            'class': 'field_input'
        })
    )
    
    password = forms.CharField(
        label='Mot de passe',
        label_suffix=' *',
        required=True, 
        max_length=60, 
        widget=forms.PasswordInput(attrs={
            'class': 'field_input'
        })
    )


class RegisterForm(UserCreationForm):
    
    email = forms.EmailField(
        max_length=60, 
        required=False,
        label='Email',
        label_suffix=' **',
        widget=forms.TextInput (attrs={
            'class': 'field_input'
        })
    )
    phone_number = forms.CharField(
        max_length=20, 
        required=False,
        label='Numéro Tel',
        label_suffix=' **',
        help_text='Le numéro commence par 00',
        widget=forms.TextInput (attrs={
            'class': 'field_input'
        })
    )
    first_name = forms.CharField(
        max_length=50, 
        label_suffix='',
        label='Nom',
        widget=forms.TextInput (attrs={
            'class': 'field_input'
        })
    )
    
    last_name = forms.CharField(
        max_length=50, 
        label_suffix='',
        label='Prénom',
        widget=forms.TextInput (attrs={
            'class': 'field_input'
        })
    )
    password1 = forms.CharField(
        label='Mot de passe',
        label_suffix=' *',
        required=True,
        widget=forms.PasswordInput (attrs={
            'class': 'field_input'
        })
    )
    password2 = forms.CharField(
        label='Conf. Mot de passe',
        label_suffix=' *',
        required=True,
        widget=forms.PasswordInput (attrs={
            'class': 'field_input'
        })
    )
    # role = forms.ChoiceField(
    #     label ='Role',
    #     label_suffix= ' *',
    #     choices=[], 
    #     required=True,
    #     help_text='Rôle Utilisateur',
    # )
    
    class Meta:
        model = get_user_model()
        fields = ['email', 'phone_number', 'first_name', 'last_name', 'password1', 'password2', ]
    
    # def __init__(self, *args, **kwargs) :
    #     super().__init__(*args, **kwargs)
    #     self.fields['role'].choices = MyUser.ROLE_CHOICES
    #     self.fields['role'].initial = MyUser.ROLE_CHOICES[2]
    
    # Nos méthode de validations
    
    def clean_email(self):
        
        email = self.cleaned_data["email"]
        # Pour éviter une requête bdd inutile si le champs est vide
        if email == '':
            return email
        
        if MyUser.objects.filter(email=email).exists():
            raise ValidationError (
                "Adresse mail existe déjà", 
                code='email_alredy_exist'
            )
        return email
    
    # On aurai pu utiliser la librairy django-phone-number
    # pour avoir quelque chose de plus robuste
    def clean_phone_number(self):
        
        phone_number = self.cleaned_data["phone_number"]
        # Pour éviter une requête bdd inutile si le champs est vide
        if phone_number == '':
            return phone_number
        elif len(phone_number) < 9 or len(phone_number) > 20 or phone_number[:2] != '00':
            raise ValueError('Mauvais formatage du numéro de tel. Ex: 00...')
        
        if MyUser.objects.filter(phone_number=phone_number).exists():
            raise ValidationError (
                "Numéro de téléphone existe déjà", 
                code='phone_number_alredy_exist'
            )
        
        return phone_number
    
    def clean(self) :
        cleaned_data = super().clean()
        email = self.cleaned_data.get('email')
        phone_number = self.cleaned_data.get('phone_number')
        print(type(phone_number))
        if email == '' and phone_number == '':
            raise ValidationError('Renseigner soit un numéro de téléphone, soit un mail')
        return cleaned_data

