from .models import ParametroSistema


def carregar_parametro(ambiente, chave):
    try:
        parametro = ParametroSistema.objects.get(ambiente=ambiente, chave=chave)
        return parametro.valor
    except ParametroSistema.DoesNotExist:
        return None
