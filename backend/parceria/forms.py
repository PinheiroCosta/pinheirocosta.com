from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Parceria, PedidoServico, PedidoServico, PedidoItem, CupomPromocional, ServicoContratado


class PedidoItemForm(forms.ModelForm):
    class Meta:
        model = PedidoItem
        fields = ('servico', 'cupom_promocional', 'data_renovacao', 'recorrente', 'periodo_gratuito')

    def clean_cupom_promocional(self):
        cupom = self.cleaned_data.get('cupom_promocional')

        if not cupom:
            return cupom

        if not cupom.ativo:
            raise ValidationError(f"O cupom '{cupom.cupom}' não está ativo.")

        if cupom.validade and cupom.validade < timezone.now().date():
            raise ValidationError(f"O cupom '{cupom.cupom}' expirou em {cupom.validade}.")

        if cupom.uso_unico and cupom.data_uso:
            raise ValidationError(f"O cupom '{cupom.cupom}' já foi utilizado.")

        return cupom

class ParceriaForm(forms.ModelForm):
    class Meta:
        model = Parceria
        fields = '__all__'

    def clean_user(self):
        user = self.cleaned_data['user']
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

    def clean_cupom_promocional(self):
        cupom = self.cleaned_data.get("cupom_promocional")
        if not cupom:
            return cupom

        if not cupom.ativo:
            raise forms.ValidationError("Este cupom não está ativo.")

        if cupom.validade and cupom.validade < timezone.now():
            raise forms.ValidationError("Este cupom expirou.")

        if cupom.uso_unico and cupom.data_uso is not None:
            raise forms.ValidationError("Este cupom já foi utilizado e é de uso único.")

        return cupom

    def save(self, commit=True):
        instance = super().save(commit=False)
        cupom = instance.cupom_promocional

        if cupom and cupom.uso_unico and cupom.data_uso is None:
            cupom.data_uso = timezone.now()
            cupom.data_criacao = timezone.now()
            cupom.save()

        if commit:
            instance.save()
        return instance
