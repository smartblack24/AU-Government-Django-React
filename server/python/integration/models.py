from django.db import models

from solo.models import SingletonModel


class Xero(SingletonModel):
    consumer_key = models.CharField(
        max_length=256,
        null=True,
        verbose_name='Consumer Key',
    )
    consumer_secret = models.CharField(
        max_length=256,
        null=True,
        verbose_name='Consumer Secret',
    )
    rsa_key = models.TextField(null=True, verbose_name='RSA Key')


class Gmail(SingletonModel):
    client_id = models.CharField(
        max_length=256,
        null=True,
        verbose_name='Client ID',
    )
    client_secret = models.CharField(
        max_length=256,
        null=True,
        verbose_name='Client Secret'
    )
    show_mails = models.BooleanField(default=True)
