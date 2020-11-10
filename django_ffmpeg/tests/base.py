import logging
import os

from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from django.core.files import File
from django.test import TestCase

from django_ffmpeg.models import ConvertingCommand, Video


logger = logging.getLogger(__name__)


class BaseTestCase(TestCase):

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
