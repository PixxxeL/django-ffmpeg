# -*- coding: utf-8 -*-

import logging
import re
import os
import commands
import datetime

from django.core.management.base import BaseCommand
from django.conf import settings

from django_ffmpeg.models import Video, ConvertingCommand, FFMPEG_ORIG_VIDEO, FFMPEG_CONV_VIDEO


class Command(BaseCommand):

    args = 'no arguments!'
    help = u'Converts unconverted video'
    _log = None

    def handle(self, *args, **options):
        # Choosing unconverted video
        try:
            video = Video.objects.filter(convert_status='pending')[0]
        except IndexError:
            self._log.info('No video found. Bypassing call...')
            return
        video.convert_status = 'started'
        video.save()

        filepath = str(video.video.file)
        full_name = filepath.split('/')[-1]
        parts = full_name.split('.')
        name = '.'.join(parts[:-1])

        video_info = {
            'name': full_name,
            'extension': parts[-1],
        }
        cmds = ConvertingCommand.objects.filter(is_enabled=True)
        cmd = None
        for c in cmds:
            data = video_info.get(c.match_by)
            if not data:
                continue
            if re.match(c.match_regex, data):
                cmd = c
                break

        if not cmd:
            video.convert_status = 'error'
            video.last_convert_msg = u'Conversion command not found'
            video.save()
            return

        try:
            params = {
                'input_file': filepath,
                'output_file': video.converted_path
            }
            output = commands.getoutput(cmd.command % params)
        except:
            video.convert_status = 'error'
            video.last_convert_msg = u'Exception while converting'
            video.save()
            raise

        video.convert_status = 'converted'
        video.last_convert_msg = output
        video.converted_at = datetime.datetime.now()
        video.save()
        self._log.info('Video converted')

    def _logger(self):
        '''
        Инициализация логгера.
        Использование: self._log.info('Your log messaage')
        '''
        self._log = logging.getLogger()
        fmt = logging.Formatter('%(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(fmt)
        self._log.addHandler(handler)
        self._log.setLevel(logging.INFO)
        #if settings.LOGGING_FILE_PATH:
        #    handler = logging.FileHandler(settings.LOGGING_FILE_PATH)
        #    fmt = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        #    handler.setFormatter(fmt)
        #    self._log.addHandler(handler)

