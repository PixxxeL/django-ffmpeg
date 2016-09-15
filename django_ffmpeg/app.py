# -*- coding: utf-8 -*-

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DjangoFfmpegConfig(AppConfig):
    name = 'django_ffmpeg'
    verbose_name = _('Videos')
