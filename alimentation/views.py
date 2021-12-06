from typing import ItemsView
from django.conf.urls import url
from django.urls import reverse_lazy
from django.shortcuts import render, reverse,redirect
from django.views.generic import DetailView,ListView,DeleteView,FormView,UpdateView,TemplateView
from django.views.generic.base import TemplateView
from .models import Aliment,Alimentation,Profile
from django.db.models import  Sum,Count
from datetime import date
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import InscriptionForm,LoginForm,MDPResetform
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.views.generic.dates import DayArchiveView
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.views import PasswordResetConfirmView,PasswordResetDoneView
class InscriptionFormView(FormView):
    form_class = InscriptionForm
    template_name = "compte/inscription.html"
    success_url = 'login'
    def form_valid(self,form):
        user = User.objects.create(username=form.cleaned_data["username"],password=form.cleaned_data["password2"],first_name=form.cleaned_data["nom"],last_name=form.cleaned_data["prenom"])
        profile = Profile.objects.create(utilisateur=user,calorie=2000,lipides=20,cholestérol=0.3,protéines=60,potassium=3.5,glucides=190)
        return super().form_valid(form)
class LoginFormView(FormView):
    form_class = LoginForm
    template_name = "compte/login.html"
    success_url = '/'
    def form_valid(self,form):
        user = authenticate(username=form.cleaned_data["username"],password=form.cleaned_data["password"])
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
class MDPResetFormView(FormView):
    form_class = MDPResetform
    template_name = "compte/changer-mdp.html"
    success_url = 'mail_reset'
    def form_valid(self,form):
        utilisateurs = User.objects.filter(email=form.cleaned_data.get('email'))
        if utilisateurs.exists():
            for utilisatateur in  utilisateurs:
                email_template_name = "mail/reset_mail.txt"
                mail_data = {
                        "email":utilisatateur.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'CaraAlim',
                        "uid": urlsafe_base64_encode(force_bytes(utilisatateur.pk)),
                        "user": utilisatateur,
                        'token': default_token_generator.make_token(utilisatateur),
                        'protocol': 'http',
                        }
                content = render_to_string(email_template_name,mail_data)
                print(content)
                send_mail(subject="Reset du mot de passe",message=content,from_email="guyanebbc@gmail.com",recipient_list=[f"{form.cleaned_data.get('email')}"])
        return super().form_valid(form)    

class MDPChangerFormView(PasswordResetConfirmView):
    template_name = "compte/changer-mdp.html"
    success_url = '/accounts/login'
    def form_valid(self,form):
        User.objects.filter(id=self.user.id).update(password=form.cleaned_data.get('new_password1'))
        return super().form_valid(form)    
    def get_form(self):
        form = super(MDPChangerFormView, self).get_form()
        for visible in form.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
        return form
class AlimentDetailView(LoginRequiredMixin,DetailView):
    model = Aliment
    template_name = "alimentation/aliment_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["liste_profile"] = Profile.objects.all()
        return context
    
class AlimentationListView(LoginRequiredMixin,ListView):
    model = Alimentation
    template_name = "alimentation/alimentation_list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["liste_aliments"] = Aliment.objects.all()
        context["liste_profile"] = Profile.objects.all()
        context["liste_consomation"] = Alimentation.objects.filter(utilisateur=self.request.user.id,date=date.today())
        liste_totale_valeur = []
        liste_profile_valeur = []
        if Alimentation.objects.filter(utilisateur=self.request.user.id,date=date.today()).exists():
            context["liste_totale"] =  Alimentation.objects.filter(utilisateur=self.request.user.id,date=date.today()).aggregate(Count("aliment__nom"),Sum("aliment__calorie"),Sum("aliment__lipides"),Sum("aliment__cholestérol"),Sum("aliment__protéines"),Sum("aliment__potassium"),Sum("aliment__glucides"))
            liste_totale_valeur = []
            liste_profile_valeur = []
            for item in context["liste_profile"].values() :
                liste_profile_valeur.append(item)
            for item in context["liste_totale"].values() :
                liste_totale_valeur.append(item)
            liste_totale_valeur = liste_totale_valeur[1:]
            liste_profile_valeur = list(liste_profile_valeur[0].values())
            liste_profile_valeur = liste_profile_valeur[2:]
            result = map(lambda x, y: round((x / y)*100,2), liste_totale_valeur, liste_profile_valeur)
            context["liste_pourcentage"] = list(result)
        return context
    def post(self,request) :
        if request.method == "POST" :
            aliment_consomme = request.POST["ajouter-aliment"]
            if aliment_consomme:
                aliment_cosomme_utilisateur = Aliment.objects.get(id=aliment_consomme)
                utilisateur = request.user
                alimentation = Alimentation(utilisateur=utilisateur,aliment=aliment_cosomme_utilisateur)
                alimentation.save()
        return HttpResponseRedirect(reverse('alimentation:index'))
class ProfileUpdateView(LoginRequiredMixin,UpdateView):
    model = Profile
    template_name = "alimentation/profile_update.html"
    fields = ["calorie","lipides","cholestérol","protéines","potassium","glucides"]
    success_url = "/"
    def get_form(self):
        form = super(ProfileUpdateView, self).get_form()
        for visible in form.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
        return form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["liste_profile"] = Profile.objects.all()
        return context
class AlimentationDeleteView(LoginRequiredMixin,DeleteView):
    model = Alimentation
    template_name = "alimentation/aliment_delete.html"
    success_url = reverse_lazy("alimentation:index")
class AlimeantionDayArchiveView(DayArchiveView):
    date_field = "date"
    allow_future = False
    month_format = "%m"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["liste_profile"] = Profile.objects.all()
        context["liste_totale"] =  Alimentation.objects.filter(utilisateur=self.request.user.id,date=kwargs.get("day")).aggregate(Count("aliment__nom"),Sum("aliment__calorie"),Sum("aliment__lipides"),Sum("aliment__cholestérol"),Sum("aliment__protéines"),Sum("aliment__potassium"),Sum("aliment__glucides"))
        liste_totale_valeur = []
        liste_profile_valeur = []
        for item in context["liste_profile"].values() :
                liste_profile_valeur.append(item)
        for item in context["liste_totale"].values() :
            liste_totale_valeur.append(item)
        liste_totale_valeur = liste_totale_valeur[1:]
        liste_profile_valeur = list(liste_profile_valeur[0].values())
        liste_profile_valeur = liste_profile_valeur[2:]
        result = map(lambda x, y: round((x / y)*100,2), liste_totale_valeur, liste_profile_valeur)
        context["liste_pourcentage"] = list(result)
        return context
    def get_queryset(self):
        return  Alimentation.objects.filter(utilisateur=self.request.user)

class MailResetView(TemplateView):
    template_name = "compte/base.html"
    
class HistoriqueListView(LoginRequiredMixin,ListView):
    template_name = "alimentation/historique_list.html"
    def get_queryset(self):
        return Alimentation.objects.filter(utilisateur=self.request.user).exclude(date=date.today()).distinct().values("date")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["liste_profile"] = Profile.objects.all()
        return context

