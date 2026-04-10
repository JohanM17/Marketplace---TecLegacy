from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from .models import Profile


class CustomSetPasswordForm(SetPasswordForm):
    """Formulario para restablecer contraseña que valida que no sea igual a la actual."""
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password1")
        if new_password and self.user.check_password(new_password):
            raise forms.ValidationError(
                "La nueva contraseña no puede ser igual a tu contraseña actual. Por seguridad, elige una diferente."
            )
        return cleaned_data


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        """Validar que el correo electrónico sea único."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado. Por favor, utiliza uno diferente.')
        return email


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'city', 'country', 'postal_code', 'profile_image']