from django.db import models


class MOTD(models.Model):
    text = models.TextField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:60]


class MOTDConfig(models.Model):
    message_override = models.ForeignKey(
        MOTD,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Se definido, esta mensagem será usada como MOTD fixa."
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Config (override: {self.message_override})"

