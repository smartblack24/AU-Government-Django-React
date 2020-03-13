from django import forms

from .models import GmailAccount
from .utils import encrypt_password


class GmailAccountForm(forms.ModelForm):
    username = forms.EmailField(widget=forms.EmailInput, label="Username")
    token = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        model = GmailAccount
        fields = ['username', 'token']

    def save(self, commit=True, *args):
        instance = super(GmailAccountForm, self).save(commit=False)
        instance.token = encrypt_password(instance.username, instance.token)
        if commit:
            instance.save()
        return instance
