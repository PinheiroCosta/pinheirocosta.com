from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Parceria, PedidoServico, PedidoItem, ServicoContratado


class PedidoItemForm(forms.ModelForm):
    class Meta:
        model = PedidoItem
        fields = ('servico', 'data_renovacao', 'recorrente')

class ParceriaForm(forms.ModelForm):
    class Meta:
        model = Parceria
        fields = '__all__'

    def clean_user(self):
        user = self.cleaned_data['usuario']
        if Parceria.objects.filter(usuario=user).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este usuário já possui uma parceria registrada.")
        return user


class PedidoServicoForm(forms.ModelForm):
    class Meta:
        model = PedidoServico
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        servico = cleaned_data.get('servico')
        contrato = cleaned_data.get('contrato_servico')
        parceria = cleaned_data.get('parceria')

        if contrato and contrato.parceria != parceria:
            raise forms.ValidationError("Contrato não pertence à mesma parceria.")

        return cleaned_data


class ServicoContratadoForm(forms.ModelForm):
    class Meta:
        model = ServicoContratado
        fields = "__all__"
