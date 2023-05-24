from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


# Create baseUserManager for register with email or numer phone

class CustomUserManager (BaseUserManager) :
    """Define a model manager for User model with no username field."""
    
    
    def create_user (self, email_or_phone, nom, password=None, **extra_fields):
        
        userModel = get_user_model()
        if not email_or_phone:
            raise ValueError('Donner un E-mail ou un numéro de téléphone')
        if not nom:
            raise ValueError("Donner le nom de l'utilisateur")
        
        if '@' in email_or_phone:
            username = self.normalize_email(email_or_phone)
            if userModel.objects.filter(email=username).exists():
                raise ValueError ("Adresse mail existe déjà")
            user = self.model(email=username, username=username, first_name=nom, **extra_fields)
        else:
            username = self.normalize_phone_number(email_or_phone)
            if userModel.objects.filter(phone_number=username).exists():
                raise ValueError ("numéro de téléphone existe déjà")
            user = self.model(phone_number=username, username=username, first_name=nom, **extra_fields)
        
        user.set_password(password)   
        user.save(using=self._db)
        
        return user
    
    
    def create_superuser (self, email_or_phone, nom, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        
        return self.create_user(email_or_phone, nom, password, **extra_fields)
    
    
    def normalize_phone_number(self, phone_number):
        """
        Normalize the phone number by removing non-digit characters.
        """
        phone = ''.join(filter(str.isdigit, phone_number))
        if len(phone) < 9 or len(phone) > 20 or phone[:2] != '00':
            raise ValueError('Mauvais formatage du numéro de tel. Ex: 00...')
        return phone


# Create your models here.
class MyUser (AbstractUser) :
    
    class Meta:
        db_table = 'MYUSER'
        verbose_name = 'utilisateur'
        verbose_name_plural = 'utilisateurs'
    
    
    DRH = 'DRH'    
    CHEF = 'CHEF'
    EMPLOYE = 'EMPLOYE'
    
    ROLE_CHOICES = (
        (DRH, 'Directeur des ressources humaines'),
        (CHEF, 'Chef de groupe'),
        (EMPLOYE, 'Employé')
    )
    
    
    email = models.EmailField(_("E-mail"), max_length=50)
    phone_number = models.CharField(_("numéro téléphone"), max_length=20)
    photo_profile = models.ImageField(_("photo profile"), upload_to='photo_user', max_length=255)
    role = models.CharField(_("rôle utilisateur"), max_length=50, choices=ROLE_CHOICES)
    chef_groupe = models.ForeignKey("MYUSER", verbose_name=_("Le chef du groupe"), on_delete=models.SET_NULL, null=True)
    poste = models.CharField(_("Post employé"), max_length=50, null=True)
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_("User permission"),
        blank=True,
        related_name='custum_user_set',
        related_query_name='user'
    )
    groups = models.ManyToManyField(
        "auth.Group", 
        verbose_name=_("groups"),
        blank=True,
        related_name='custum_user_set',
        related_query_name='user'
    )
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if self.email != '':
            self.username = self.email
        elif self.phone_number != '':
            self.username = self.phone_number
        else:
            raise Exception('Données erronées transmisent!')
        # je vais lever une exception
        super().save(*args, **kwargs)