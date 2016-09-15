# -*- coding: utf-8 -*-

import logging
import re
import subprocess
import datetime
import time

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.encoding import smart_text

from django_ffmpeg.models import Video, ConvertingCommand


class Command(BaseCommand):

    args = 'no arguments'
    help = u'Converts unconverted video'
    _log = None

    def handle(self, *args, **options):

        start = time.time()
        self._logger()

        # Choosing unconverted video
        try:
            video = Video.objects.filter(convert_status='pending')[0]
        except IndexError:
            self._log.info('No video found. Bypassing call...')
            return
        video.convert_status = 'started'
        video.save()

        filepath = video.video.path
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

        video.convert_extension = cmd.convert_extension
        try:
            c = cmd.command % {
                'input_file': filepath,
                'output_file': video.converted_path,
            }
            self._log.info('Convert video command: %s' % c)
            p = subprocess.Popen(c, stdout=subprocess.PIPE)
            output = p.stdout.read()
            self._log.info('Convert video result: %s' % output)
        except Exception as e:
            self._log.error('Convert error: %s' % e)
            video.convert_status = 'error'
            video.last_convert_msg = u'Exception while converting'
            video.save()
            raise

        try:
            if not video.thumb:
                cmd = 'ffmpeg -hide_banner -nostats -i %s -frames:v 1 -ss 0 %s' % (
                    filepath, video.thumb_video_path,
                )
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self._log.info('Create thumbnail command: %s' % cmd)
        except:
            pass

        video.convert_status = 'converted'
        video.last_convert_msg = smart_text(output)
        video.converted_at = datetime.datetime.now()
        video.save()
        self._log.info('Job finished at: %s s\n' % (time.time() - start))


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

