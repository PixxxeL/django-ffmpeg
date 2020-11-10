import logging
import os
import time

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from django.core.files import File
from django.test import TestCase, tag

from django_ffmpeg.models import (
    ConvertingCommand, Video, VIDEO_CONVERSION_STATUS_CHOICES as STATUS
)
from django_ffmpeg.utils import Converter


logger = logging.getLogger(__name__)


CONV_TIMEOUT = getattr(settings, 'FFMPEG_TEST_CONV_TIMEOUT', 30)
EMULATION = getattr(settings, 'FFMPEG_TEST_EMULATION', True)


class ConverterTest(TestCase):

    @tag('ffmpeg-converter')
    def test_success_convert_pending(self):
        user = self.create_superuser()
        self.create_command()
        video = self.create_video_file(user)
        self.assertEqual(video.convert_status, STATUS[0][0])
        converter = Converter()
        converter.emulation = EMULATION
        converter.convert_first_pending()
        time.sleep(CONV_TIMEOUT)
        video.refresh_from_db()
        self.assertEqual(video.convert_status, STATUS[2][0])
        self.remove_video_file(video)

    def create_superuser(self):
        user = User.objects.create_user(
            username='tester',
            email='tester@mail.ru',
            password='123',
            is_superuser=True
        )
        user.save()
        return user

    def create_video_file(self, user):
        filepath = finders.find('django_ffmpeg/tests/earth.mp4')
        with open(filepath, 'rb') as fh:
            video = Video(
               video=File(fh),
            )
            video.user = user
            video.save()
        return video

    def remove_video_file(self, video):
        os.remove(video.video.path)
        try:
            os.remove(video.converted_path)
        except:
            logger.error('No file: {}'.format(video.converted_path))
        try:
            os.remove(video.thumb_video_path)
        except:
            logger.error('No file: {}'.format(video.thumb_video_path))

    def create_command(self):
        cmd = ConvertingCommand(
            match_by='name',
            match_regex='.*',
            command='ffmpeg -y -i %(input_file)s -strict -2 %(output_file)s',
            thumb_command='ffmpeg -y -i %(in_file)s -frames:v 1 -ss %(thumb_frame)s %(out_file)s',
            convert_extension='mp4'
        )
        cmd.save()
        return cmd
