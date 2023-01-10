from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class CreatedModel(models.Model):
    created = models.DateTimeField(
        verbose_name='Дата добавления пользователя в БД',
        auto_now_add=True
    )

    updated = models.DateTimeField(
        verbose_name='Дата обновления записи',
        auto_now=True
    )

    class Meta:
        abstract = True


class Clients(CreatedModel):
    telegram_id = models.BigIntegerField(
        verbose_name='Telegram ID клиента',
        help_text='Telegram ID'

    )

    username = models.CharField(
        verbose_name='Имя пользователя',
        help_text='Имя пользователя',
        null=True,
        max_length=500
    )

    is_admin = models.BooleanField(
        verbose_name='Является ли пользователь админом',
        help_text='Является ли пользователь админом',
        default=False
    )

    amount = models.IntegerField(
        verbose_name='Количество запросов',
        help_text='Количество запросов',
        default=0
    )

    is_trial = models.BooleanField(
        verbose_name='Использована ли пробная попытка',
        help_text='Использована ли пробная попытка',
        default=False
    )

    subscribe = models.BooleanField(
        verbose_name='Есть ли подписка у пользователя',
        help_text='Есть ли подписка у пользователя',
        default=False,

    )

    start_subscribe = models.DateTimeField(
        verbose_name='Дата начала подписки',
        help_text='Дата начала подписки',
        null=True
    )

    end_subscribe = models.DateTimeField(
        verbose_name='Дата окончания подписки',
        help_text='Дата окончания подписки',
        null=True
    )

    is_notificated = models.BooleanField(
        verbose_name='Предупрежден ли пользователь об окончании подписки',
        help_text='Предупрежден ли пользователь об окончании подписки',
        default=False
    )


class Rate(CreatedModel):
    title = models.CharField(
        verbose_name='Название тарифа',
        help_text='Название тарифа',
        default='Стандарт',
        max_length=1000
    )

    description = models.CharField(
        verbose_name='Описание тарифа',
        help_text='Описание тарифа',
        default='При покупке тарифа вы получете доступ к боту и возможность отправить до 10000 запросов.\n'
                'Длительность подписки - 1 месяц.',
        max_length=100000
    )

    amount = models.IntegerField(
        verbose_name='Количество запросов',
        help_text='Количетсво запросов',
        null=True
    )

    price = models.IntegerField(
        verbose_name='Цена тарифа',
        help_text='Цена тарифа',
        default=2000
    )


class ClientRequest(models.Model):
    channel_name = models.CharField(
        verbose_name='Название канала',
        help_text='Название канала',
        max_length=10000,
        default='Нет информации'
    )

    count = models.IntegerField(
        verbose_name='Участники',
        help_text='Участники',
        default='Нет информации'
    )

    link = models.CharField(
        verbose_name='Ссылка на канал',
        help_text='Ссылка на канал',
        max_length=10000,
        default='Нет информации'
    )

    ERR = models.CharField(
        verbose_name='ERR',
        help_text='ERR',
        max_length=1000,
        default='Нет информации'
    )

    ERR24 = models.CharField(
        verbose_name='ERR24',
        help_text='ERR24',
        max_length=1000,
        default='Нет информации'
    )

    citate_amount = models.CharField(
        verbose_name='Цитирование в накрученных каналах',
        help_text='Цитирование в накрученных каналах',
        max_length=100000,
        default='Нет информации'
    )

    citate_percent = models.CharField(
        verbose_name='Цитирование в процентах',
        help_text='Цитирование в процентах',
        max_length=100000,
        default='Нет информации'
    )

    client = models.ForeignKey(
        Clients,
        on_delete=models.CASCADE,
        related_name='user',
        blank=True,
        null=True,
        help_text='Пользователь',
        verbose_name='Пользователь'
    )


class Payments(models.Model):
    rate = models.IntegerField(
        verbose_name='ID тарифа',
        help_text='ID тарифа',
        null=True
    )
    client = models.IntegerField(
        verbose_name='ID клиента',
        help_text='ID клиента',
        null=True
    )

    payment_id = models.CharField(
        verbose_name='ID платежа',
        help_text='ID платежа',
        max_length=50000,
        null=True
    )

    amount = models.IntegerField(
        verbose_name='Количество запросов',
        null=True
    )
