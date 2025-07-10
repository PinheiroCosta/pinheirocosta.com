from django import forms
from .models import Parceria, PedidoServico


class ParceriaForm(forms.ModelForm):
    class Meta:
        model = Parceria
        fields = '__all__'

    def clean_user(self):
        user = self.cleaned_data['user']
        if Parceria.objects.filter(user=user).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este usuário já possui uma parceria registrada.")
        return user


class PedidoServicoForm(forms.ModelForm):
    class Meta:
        model = PedidoServico
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        servico = cleaned_data.get('servico')
        contrato = cleaned_data.get('contrato')
        parceria = cleaned_data.get('parceria')

        if servico and servico.periodicidade != 'avulso' and not contrato:
            raise forms.ValidationError("Contrato é obrigatório para serviços mensais ou anuais.")

        if contrato and contrato.parceria != parceria:
            raise forms.ValidationError("Contrato não pertence à mesma parceria.")

        return cleaned_data
