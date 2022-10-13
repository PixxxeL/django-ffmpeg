import os

from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from django_ffmpeg import defaults as ffmpeg_settings


class DjangoFfmpegConfig(AppConfig):
    name = 'django_ffmpeg'
    verbose_name = _('Videos')

    def ready(self):
        self._make_directories()

    def _make_directories(self):
        dirs = (
            ffmpeg_settings.FFMPEG_ORIG_VIDEO,
            ffmpeg_settings.FFMPEG_THUMB_VIDEO,
            ffmpeg_settings.FFMPEG_CONV_VIDEO,
        )
        for _ in dirs:
            os.makedirs(os.path.join(
                settings.MEDIA_ROOT,
                ffmpeg_settings.FFMPEG_PRE_DIR,
                _
            ), exist_ok =True)
