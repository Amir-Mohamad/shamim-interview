from django import forms
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='email',
        validators=[EmailValidator('correct email'), ],
    )
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        is_exists = User.objects.filter(email=email).exists()
        if is_exists:
            raise forms.ValidationError('Already exists.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('don\'t match.')
        if len(password2) < 8:
            raise forms.ValidationError('8 chars.')
        return password2
