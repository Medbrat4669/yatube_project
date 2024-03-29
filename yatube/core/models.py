from django.db import models


class CreatedModel(models.Model):
    """Абстрактная модель для добавления даты и временни создания."""
    created = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )

    class Meta:
        abstract = True
