# -*- coding: utf-8 -*-

import datetime
import logging
import os
import re

from django_ffmpeg.models import Video, ConvertingCommand
from pytz import timezone


logger = logging.getLogger(__name__)


class Converter(object):

    def convert(self):
        # Choosing one unconverted video
        try:
            video = Video.objects.filter(convert_status='pending')[0]
        except IndexError:
            logger.info('No video found. Bypassing call...')
            return
        video.convert_status = 'started'
        video.save()

        # Choosing converting command
        filepath = video.video.path
        full_name = filepath.split('/')[-1]

        video_info = {
            'name': full_name,
            'extension': full_name.split('.')[-1],
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
            logger.error('Conversion command not found...')
            video.convert_status = 'error'
            video.last_convert_msg = 'Conversion command not found'
            video.save()
            return

        # Convert video
        video.convert_extension = cmd.convert_extension
        try:
            c = cmd.command % {
                'input_file': filepath,
                'output_file': video.converted_path,
            }
            logger.info('Converting video command: %s' % c)
            output = self._cli(c)
            logger.info('Converting video result: %s' % output)
        except Exception as e:
            logger.error('Converting video error', exc_info=True)
            video.convert_status = 'error'
            video.last_convert_msg = u'Exception while converting'
            video.save()
            raise

        # Convert thumb
        try:
            if not video.thumb:
                cmd = cmd.thumb_command % {
                    'in_file'     : filepath,
                    'out_file'    : video.thumb_video_path,
                    'thumb_frame' : video.thumb_frame,
                }
                self._cli(cmd, True)
                logger.info('Creating thumbnail command: %s' % cmd)
        except:
            logger.error('Converting thumb error', exc_info=True)

        video.convert_status = 'converted'
        video.last_convert_msg = repr(output).replace('\\n', '\n').strip('\'')
        video.converted_at = datetime.datetime.now(tz=timezone('UTC'))
        video.save()


    def _cli(self, cmd, without_output=False):
        if os.name == 'posix':
            import commands
            return commands.getoutput(cmd)
        else:
            import subprocess
            if without_output:
                DEVNULL = open(os.devnull, 'wb')
                subprocess.Popen(cmd, stdout=DEVNULL, stderr=DEVNULL)
            else:
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                return p.stdout.read()
