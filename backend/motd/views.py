from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils.cache import caches
from .models import MOTD, MOTDConfig
from .serializers import MOTDSerializer, MOTDConfigSerializer
import random


class MOTDViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = MOTD.objects.all()
    serializer_class = MOTDSerializer

    @action(detail=False, methods=["get"], url_path="random")
    def get_motd(self, request):
        cache = caches["default"]
        motd = cache.get("motd_of_the_day")

        if not motd:
            config = MOTDConfig.objects.first()
            if config and config.message_override and config.message_override.active:
                motd = config.message_override.text
            else:
                messages = MOTD.objects.filter(active=True)
                motd = random.choice(messages) if messages.exists() else None

            cache.set("motd_of_the_day", motd, timeout=60 * 60 * 24)

        if motd is None:
            return Response({"detail": "Nenhuma mensagem disponível"}, status=204)

        serializer = MOTDSerializer(motd)
        return Response(serializer.data)


class MOTDConfigViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = MOTDConfig.objects.all()
    serializer_class = MOTDConfigSerializer

    @action(detail=False, methods=["get"], url_path="singleton")
    def singleton(self, request):
        config = MOTDConfig.objects.first()
        if not config:
            return Response(
                {"detail": "Nenhuma configuração encontrada"},
                status=status.HTTP_204_NO_CONTENT,
            )
        serializer = self.get_serializer(config)
        return Response(serializer.data)
