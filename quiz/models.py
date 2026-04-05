from django.db import models

class Question(models.Model):
    """Модель для хранения вопросов квиза."""
    country = models.CharField(
        max_length=100,
        verbose_name="Страна (именительный падеж)",
        unique=True
    )
    country_genitive = models.CharField(
        max_length=100,
        verbose_name="Страна (родительный падеж)",
        help_text="Как в вопросе: 'Столица [чего]?'"
    )
    capital = models.CharField(
        max_length=100,
        verbose_name="Столица"
    )

    def __str__(self):
        return f"{self.country} — {self.capital}"

