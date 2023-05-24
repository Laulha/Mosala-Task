from django.shortcuts import render, redirect,HttpResponseRedirect
from django.urls import reverse
from .forms import ConnectionForm, RegisterForm
from taskmanager.models import LienConnexion
from django.contrib.auth import authenticate, login, logout
from mesmodules.decorators import if_user_authentificated

"""
Cette fonction va soit renvoyer vers la page de login (si l'utilisateur)
n'est pas connecté, dans la mesure où il est connecté, elle va 
renvoyer vers la page task_manager (home_app)
"""
def index(request):
    return redirect('auth:login')


@if_user_authentificated('task-manager:index')
def log_in (request) : 
    
    form = ConnectionForm()
    message = ''
    if request.method == 'POST':
        form = ConnectionForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email_or_phone = form.cleaned_data['email_or_phone'],
                password = form.cleaned_data['password']
            )
            if user is not None :
                response = HttpResponseRedirect(reverse('task-manager:index'))
                response.delete_cookie('lien_connexion')
                login(request, user, backend='authentification.backend.CustomBackend')
                return response
            else:
                message = 'Données incorrects'
    
    context = {
        'form' : form,
        'message' : message,
    }
    
    return render(request, 'authentification/login_page.html', context)


@if_user_authentificated('task-manager:index')
def register (request) : 
    # on vérifie que notre cookie d'inscription existe.
    lien_a_tester = request.COOKIES.get('lien_connexion')
    if not lien_a_tester:
        return redirect('auth:forbiden_auth')
    
    try:
        lien = LienConnexion.objects.get(lien_connexion=lien_a_tester)
        if lien.statut_lien > 1:
            return redirect('auth:forbiden_link')
    except LienConnexion.DoesNotExist:
        return redirect('auth:forbiden_auth')
    
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = lien.role_lien
            user.poste = lien.poste_lien
            user.save()
            # Liaison et expiration lien
            lien.employe = user
            lien.statut_lien += 1
            lien.save()
            
            response = HttpResponseRedirect(reverse('task-manager:index'))
            response.delete_cookie('lien_connexion')
            login(request, user, backend='authentification.backend.CustomBackend')
            return response
    
    context = {
        'form' : form,
    }
    return render(request, 'authentification/register.html', context)


def teste_link(request, lien_a_tester):
    # On vérifier que le lien existe
    try:
        lien = LienConnexion.objects.get(lien_connexion=lien_a_tester)
        
        if lien.statut_lien == 0:
            lien.statut_lien += 1
            lien.save()
            response = HttpResponseRedirect(reverse('auth:register'))
            response.set_cookie('lien_connexion', lien_a_tester)
            return response
        elif lien.statut_lien == 1:
            lien.statut_lien += 1
            lien.save()
            response = HttpResponseRedirect(reverse('auth:forbiden_link'))
            response.delete_cookie('lien_connexion')
            return response
        else:
            return redirect('auth:forbiden_link')
            
    except LienConnexion.DoesNotExist:
        return redirect('auth:forbiden_auth')


def logout_user (request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('auth:login')


@if_user_authentificated('task-manager:index')
def forbiden_auth(request):
    return render(request, 'authentification/forbiden-auth.html')

@if_user_authentificated('task-manager:index')
def forbiden_link(request):
    return render(request, 'authentification/forbiden-link.html')