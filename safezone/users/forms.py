from django import forms
from django.contrib.auth.forms import SetPasswordForm, AuthenticationForm
from .models import Invite, User


class InviteForm(forms.ModelForm):
    class Meta:
        model = Invite
        fields = ['email', 'facility']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.role = 'admin'
        from uuid import uuid4
        instance.token = uuid4().hex
        if commit:
            instance.save()
        return instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class RegistrationForm(SetPasswordForm):
    first_name = forms.CharField(max_length=100, label='Имя')
    last_name = forms.CharField(max_length=100, label='Фамилия')

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].label = 'Пароль'
        self.fields['new_password1'].help_text = ''
        self.fields['new_password2'].label = 'Подтверждение пароля'
        self.fields['new_password2'].help_text = ''

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        self.order_fields(['first_name', 'last_name', 'new_password1', 'new_password2'])


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'