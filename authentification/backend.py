from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


class CustomBackend(BaseBackend):
    
    def authenticate (self, request, email_or_phone=None, password=None, **kwargs):
        
        userModel = get_user_model()
        try:
            user = userModel.objects.get(username=email_or_phone)
        except userModel.DoesNotExist:
            return None
        
        if user.check_password(password):
            return user
        return None
    
    
    def get_user (self, id_user):
        userModel = get_user_model()
        try:
            return userModel.objects.get(pk=id_user)
        except userModel.DoesNotExist:
            return None