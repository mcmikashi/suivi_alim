from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordResetForm
from django.contrib.auth.models import User
class InscriptionForm(UserCreationForm):
    nom = forms.CharField(max_length=50, required=True)
    prenom = forms.CharField(max_length=50, required=True)
    field_order = ["nom","prenom"]
    def __init__(self, *args,**kwargs):
        super(InscriptionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]="form-control"
class LoginForm(AuthenticationForm):
    def __init__(self, *args,**kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]="form-control"
class MDPResetform(PasswordResetForm):
    def __init__(self, *args,**kwargs):
        super(MDPResetform, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]="form-control"