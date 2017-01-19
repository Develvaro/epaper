from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from epaper.models import Noticia, Comentario

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def is_valid(self):
        # run the parent validation first
        valid = super(UserCreateForm, self).is_valid()
        # we're done now if not valid
        if not valid:
            return valid

        mail_check = User.objects.filter(email = self.cleaned_data["email"])
        if not mail_check:
            return True
        else:
            return False

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class Nueva_Noticia_Form(ModelForm):
    class Meta:
        model = Noticia
        exclude = ["visitas", "likes", "pub_date", "autor"]
        fields = '__all__'

class Busqueda(forms.Form):
    titulo = forms.CharField()

    def is_valid(self):
        # run the parent validation first
        valid = super(Busqueda, self).is_valid()

        # we're done now if not valid
        if not valid:
            return valid

        if len(self.cleaned_data['titulo']) == 0:
            return False
        else:
            return True

class Comentario_form(forms.Form):
    texto = forms.CharField(widget=forms.Textarea)
    def is_valid(self):
        # run the parent validation first
        valid = super(Comentario_form, self).is_valid()
        # we're done now if not valid
        if not valid:
            return valid

        if len(self.cleaned_data['texto']) == 0:
            return False
        else:
            return True

class Editar_Perfil_Form(forms.Form):
    nombre = forms.CharField(initial = 'nombre')
    apellidos = forms.CharField(initial = 'apellidos')
    email = forms.EmailField(initial = 'email')
    foto_perfil = forms.ImageField(required = False)

    def is_valid(self):
        # run the parent validation first
        valid = super(Editar_Perfil_Form, self).is_valid()
        # we're done now if not valid
        if not valid:
            return valid
        return True
