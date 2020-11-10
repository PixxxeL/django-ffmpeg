import logging
import time

from django.conf import settings
from django.test import tag

from django_ffmpeg.models import (
    VIDEO_CONVERSION_STATUS_CHOICES as STATUS
)
from django_ffmpeg.tasks import convert_video
from django_ffmpeg.tests.base import BaseTestCase


logger = logging.getLogger(__name__)


CONV_TIMEOUT = getattr(settings, 'FFMPEG_TEST_CONV_TIMEOUT', 30)


class CeleryTaskTest(BaseTestCase):

    @tag('ffmpeg-converter')
    def test_success_convert(self):
        user = self.create_superuser()
        cmd = self.create_command()
        video = self.create_video_file(user)
        convert_video.apply(args=(cmd.pk, video.pk,))
        time.sleep(CONV_TIMEOUT)
        video.refresh_from_db()
        self.assertEqual(video.convert_status, STATUS[2][0])
        self.remove_video_file(video)
