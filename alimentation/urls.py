from django.db.models.base import Model
from django.db.models.fields import DateField
from django.urls import path
from .views import AlimentDetailView,AlimentationListView,AlimentationDeleteView,LoginFormView,InscriptionFormView,ProfileUpdateView,AlimeantionDayArchiveView,HistoriqueListView,MDPChangerFormView,MDPResetFormView,MailResetView
app_name = "alimentation"
urlpatterns = [
    path('',AlimentationListView.as_view(),name="index"),
    path('historique/<int:year>-<int:month>-<int:day>/',AlimeantionDayArchiveView.as_view(),name="historique-alimenation"),
    path('detail/<int:pk>',AlimentDetailView.as_view(),name="detail"),
    path('delete/<int:pk>',AlimentationDeleteView.as_view(),name="delete"),
    path('historique/',HistoriqueListView.as_view(),name="historique"),
    path('accounts/inscription',InscriptionFormView.as_view(),name="inscription"),
    path('accounts/login',LoginFormView.as_view(),name="login"),
    path('accounts/mdpreset',MDPResetFormView.as_view(),name="mdp_reset"),
    path('accounts/mail_reset',MailResetView.as_view(),name="mail_reset"),
    path('accounts/mdpchanger/<uidb64>/<token>/',MDPChangerFormView.as_view(),name="mdp_changer"),
    path('profile/modifier/<int:pk>',ProfileUpdateView.as_view(),name="profile_update"),
]