from django.shortcuts import HttpResponse, redirect, render, get_object_or_404, HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import LienConnexionForm, ModificationEmploye
from .models import LienConnexion
from authentification.models import MyUser
from mesmodules.decorators import drh_required, employe_deni

# Create your views here.

"""
* Ce index est le même pour tout type d'employé (DRH, Chef et employé). 
* En fonction du role de l'employé, les donées récupérer seront différent de la manière suivante :
    - Employé : tâches
    - Chef : employés qui sont sous ses directives
    - DRH : tout les emplyés qui sont dans la boîtes.
"""
@login_required
def index (request):
    # Initition du filtre
    filtre = {}
    ACTIVE = 'activeted'
    # Filtre au niveau de la sidebar
    act_home = ACTIVE
    
    if request.user.role == MyUser.CHEF:
        employes = MyUser.objects.filter(chef_groupe=request.user.id)
        filtre['emp'] = ACTIVE
    elif request.user.role == MyUser.EMPLOYE:
        employes = None
        filtre['tache'] = ACTIVE
    else:
        ## ici c'es forcement le drh
        employes = MyUser.objects.exclude(id=request.user.id)
        filtre['tout'] = ACTIVE
    
    contexte = {
        'employes': employes,
        'act_home' : act_home,
        'filtre': filtre
    }
    return render(request, 'taskmanager/home.html', contexte)


@login_required
@drh_required(raise_exception=True)
def employe_drh(request, employe):
    filtre = {}
    ACTIVE = 'activeted'
    # Filtre au niveau de la sidebar
    act_home = ACTIVE
    
    if employe == 'chef':
        employes = MyUser.objects.filter(role=MyUser.CHEF)
        filtre['chef'] = ACTIVE
    else:
        employes = MyUser.objects.filter(role=MyUser.EMPLOYE)
        filtre['emp'] = ACTIVE

    contexte = {
        'employes': employes,
        'act_home': act_home,
        'filtre': filtre
    }
    return render(request, 'taskmanager/home.html', contexte)

@login_required
@drh_required(raise_exception=True)
def ajout_employe(request):
    
    form = LienConnexionForm()
    if request.method == 'POST':
        lienconnexion = LienConnexion()
        form = LienConnexionForm(request.POST)
        if form.is_valid():
            lien_db = form.save(commit=False)
            lien_db.lien_connexion = lienconnexion.genere_lien()
            try:
                lien_db.save()
                # On souhaite rester sur la même page après avoir soumit notre formulaire, cette pratique
                # ne respectant pas le PRG (Post, Redirect et Get), on redirige vers notre page de base.
                return redirect('task-manager:ajout_employe')
            except Exception:
                lien_db.lien_connexion = lienconnexion.genere_lien()
                lien_db.save()
                return redirect('task-manager:ajout_employe')
    
    
    lesLiens = LienConnexion.objects.all().order_by(('-id'))
    message = request.COOKIES.get('message_reponse', '')
    
    contexte = {
        'form': form,
        'lesLiens' : lesLiens,
        'act_ajout_emp' : 'activeted',
        'message': message
    }
    
    response = render(request, 'taskmanager/ajout_employe.html', contexte)
    response.delete_cookie('message_reponse')
    
    return response

@login_required
@drh_required(raise_exception=True)
def effacer_lien (request, lien_a_effacer):
    
    deleted = LienConnexion.objects.filter(lien_connexion=lien_a_effacer).delete()
    
    if deleted[0] != 0:
        message = f"{lien_a_effacer}  à bien été effacé"
    else:
        message = f"{lien_a_effacer}  n'existe pas"
    
    response = HttpResponseRedirect(reverse('task-manager:ajout_employe'))
    response.set_cookie('message_reponse', message, max_age=None)
    
    return response



@login_required
@drh_required(raise_exception=True)
def modif_employe(request, id_employe):
    emp_modif = get_object_or_404(MyUser, id=id_employe)
    initial = {'role_employe': emp_modif.role, 'poste_employe': emp_modif.poste}
    form = ModificationEmploye(initial=initial)
    
    if emp_modif.role==MyUser.EMPLOYE:
        employes=None
    else:
        employes = MyUser.objects.filter(
            Q(role=MyUser.EMPLOYE),
            (Q(chef_groupe__id=emp_modif.id) | Q(chef_groupe__isnull=True) | Q(chef_groupe=None))
        )
    
    
    contexte = {
        'emp_modif': emp_modif, 
        'form': form, 
        'employes': employes
    }
    return render(request, 'taskmanager/modif_employe.html', contexte)


@login_required
@drh_required(raise_exception=True)
def modif_info_chef(request, id_employe):
    emp_modif = get_object_or_404(MyUser, id=id_employe)
    
    if request.method == 'POST':
        if len(request.POST) > 1:
            lesIdAjout = request.POST.getlist('ajouts')
            lesIdRetrait = request.POST.getlist('retraits')
            if lesIdAjout:
                try:
                    lesIdAjout = [int(i) for i in lesIdAjout]
                    MyUser.objects.filter(id__in=lesIdAjout).update(chef_groupe=emp_modif.id)
                except Exception:
                    pass
                
            elif lesIdRetrait:
                try:
                    lesIdRetrait = [int(i) for i in lesIdRetrait]
                    MyUser.objects.filter(id__in=lesIdRetrait).update(chef_groupe='')
                except Exception:
                    pass
                
            else:
                # Je vais devoir faire une validation de formulaire
                form = ModificationEmploye(request.POST)
                if form.is_valid():
                    role = form.cleaned_data['role_employe']
                    poste = form.cleaned_data['poste_employe']
                    if role != emp_modif.role:
                        if role == MyUser.EMPLOYE:
                            # On lui rétire tous les employés qui étaient sous sa directive
                            MyUser.objects.filter(chef_groupe__id=emp_modif.id).update(chef_groupe='')
                        else:
                            emp_modif.chef_groupe = None
                            emp_modif.save()
                    emp_modif.role = role
                    emp_modif.poste = poste
                    emp_modif.save()
                    #LienConnexion.objects.filter(lien_connexion=emp_modif.lienconnexion.all()[0].lien_connexion).update(poste_lien=poste)
    
    
    url = reverse('task-manager:modif_employe', args=[emp_modif.id])
    return redirect(url)


@login_required
@employe_deni(raise_exception=True)
def page_employe(request, id_employe):
    return HttpResponse("<h1>Page en construction</h1>")