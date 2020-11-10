import datetime
import logging
import os
import re
import subprocess
import sys

from pytz import timezone

from django_ffmpeg.models import Video, ConvertingCommand


logger = logging.getLogger(__name__)


class Converter(object):

    emulation = False

    def convert_first_pending(self):
        """"""
        video = self.choose_video()
        if not video:
            logger.info('No video found. Bypassing call...')
            return
        cmd = self.choose_convert_command(video)
        if not cmd:
            logger.error('Conversion command not found...')
            video.convert_status = 'error'
            video.last_convert_msg = 'Conversion command not found'
            video.save()
            return
        self.convert_video_thumb(cmd, video)
        self.convert_video_file(cmd, video)

    def call_cli(self, cmd, without_output=False):
        """OS independency invoking of command line interface
        """
        if self.emulation:
            return logger.debug('Call: %s' % cmd)
        if sys.version_info[0] > 2:
            res = subprocess.getstatusoutput(cmd)
            if not without_output and res and len(res):
                return res[1]
        elif os.name == 'posix':
            import commands
            return commands.getoutput(cmd)
        else:
            if without_output:
                DEVNULL = open(os.devnull, 'wb')
                subprocess.Popen(cmd, stdout=DEVNULL, stderr=DEVNULL)
            else:
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                return p.stdout.read()

    def choose_video(self):
        """First unconverted video
        """
        return Video.objects.filter(convert_status='pending')\
            .order_by('created_at')\
            .first()

    def choose_convert_command(self, video):
        """Command for video converting by matching with video file name
        """
        filepath = video.video.path
        filename = filepath.split('/')[-1]
        video_info = {
            'name': filename,
            'extension': filename.split('.')[-1],
        }
        cmds = ConvertingCommand.objects.filter(is_enabled=True)
        for c in cmds:
            match_by = video_info.get(c.match_by)
            if not match_by:
                continue
            if re.match(c.match_regex, match_by):
                return c

    def convert_video_file(self, cmd, video):
        """"""
        video.convert_status = 'started'
        video.save()
        video.convert_extension = cmd.convert_extension
        try:
            c = cmd.command % {
                'input_file': video.video.path,
                'output_file': video.converted_path,
            }
            logger.info('Converting video command: %s' % c)
            output = self.call_cli(c)
            logger.info('Converting video result: %s' % output)
        except Exception as e:
            logger.error('Converting video error', exc_info=True)
            video.convert_status = 'error'
            video.last_convert_msg = 'Exception while converting'
            video.save()
            return
        video.convert_status = 'error' \
            if output and output.find('Conversion failed') != -1 \
            else 'converted'
        video.last_convert_msg = repr(output).replace('\\n', '\n').strip('\'')
        video.converted_at = datetime.datetime.now(tz=timezone('UTC'))
        video.save()

    def convert_video_thumb(self, cmd, video):
        """"""
        try:
            if not video.thumb:
                cmd = cmd.thumb_command % {
                    'in_file'     : video.video.path,
                    'out_file'    : video.thumb_video_path,
                    'thumb_frame' : video.thumb_frame,
                }
                self.call_cli(cmd, True)
                logger.info('Creating thumbnail command: %s' % cmd)
        except:
            logger.error('Converting thumb error', exc_info=True)
