from django import forms
from .models import Parceria


class ParceriaForm(forms.ModelForm):
    class Meta:
        model = Parceria
        fields = '__all__'

    def clean_user(self):
        user = self.cleaned_data['user']
        if Parceria.objects.filter(user=user).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este usuário já possui uma parceria registrada.")
        return user
