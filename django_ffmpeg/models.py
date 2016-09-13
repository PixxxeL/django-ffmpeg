# -*- coding: utf-8 -*-

import os
import re
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


FFMPEG_PRE_DIR = getattr(settings, 'FFMPEG_PRE_DIR', 'videos')
FFMPEG_ORIG_VIDEO = FFMPEG_PRE_DIR + '/' + getattr(settings, 'FFMPEG_ORIG_VIDEO', 'orig')
FFMPEG_THUMB_VIDEO = FFMPEG_PRE_DIR + '/' + getattr(settings, 'FFMPEG_THUMB_VIDEO', 'thumb')
FFMPEG_CONV_VIDEO = FFMPEG_PRE_DIR + '/' + getattr(settings, 'FFMPEG_CONV_VIDEO', 'conv')


def path_and_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1][-5:]
        filename = '%s.%s' % (uuid4().hex, ext)
        return os.path.join(path, filename)
    return wrapper


CONVERTING_COMMAND_MATCH_CHOICES = (
    ('extension', _('Extension')),
    ('name', _('File name')),
)

class ConvertingCommand(models.Model):
    '''
    System commands for convertion videos to desired format
    '''
    match_by = models.CharField(
        max_length=50,
        verbose_name=_('Match by'),
        choices=CONVERTING_COMMAND_MATCH_CHOICES,
        default='extension',
        help_text=_('Video param to detected from if this command should be used to convert given video'),
    )
    match_regex = models.CharField(
        max_length=200,
        verbose_name=_('RegExp to match video file'),
    )
    is_enabled = models.BooleanField(
        verbose_name=_('Enabled?'),
        default=True,
    )
    command = models.TextField(
        verbose_name=_('System command to convert video'),
        help_text = 'Example: /usr/bin/avconv -nostats -y -i %(input_file)s -acodec libmp3lame -ar 44100 -f flv %(output_file)s',
    )

    def __unicode__(self):
        return u'%s "%s..."' % (self.sort_pos, self.command[0:50])

    class Meta:
        verbose_name = _(u'Video convert command')
        verbose_name_plural = _(u'Video convert commands')


VIDEO_CONVERSION_STATUS_CHOICES = (
    ('pending', _('Pending convert')),
    ('started', _('Convert started')),
    ('converted', _('Converted')),
    ('error', _('Not converted due to error')),
)

class Video(models.Model):
    '''
    Uploaded video
    '''
    title = models.CharField(
        max_length=500,
        verbose_name=_('Title'),
    )
    video = models.FileField(
        verbose_name=_('Video file'),
        upload_to=path_and_rename(FFMPEG_ORIG_VIDEO),
    )
    thumb = models.ImageField(
        verbose_name=_('Thumbnail image'),
        upload_to=path_and_rename(FFMPEG_THUMB_VIDEO),
        null=True, blank=True,
    )
    description = models.TextField(
        verbose_name=_('Description'),
        null=True, blank=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_('Created time'),
        auto_now_add=True,
    )
    convert_status = models.CharField(
        max_length=16,
        verbose_name=_('Video conversion status'),
        choices=VIDEO_CONVERSION_STATUS_CHOICES,
        default='pending',
    )
    converted_at = models.DateTimeField(
        verbose_name=_('Convert time'),
        editable=False, null=True, blank=True,
    )
    last_convert_msg = models.TextField(
        verbose_name=_('Message from last converting command'),
    )
    user = models.ForeignKey(
        User,
        verbose_name=_('Uploaded by'),
        editable=False,
    )
    meta_info = models.TextField(
        verbose_name=_('Meta info about original video'),
        null=True,
        editable=False,
    )
    convert_extension = models.CharField(
        max_length=5,
        verbose_name=_('Extension'),
        help_text = _('Without dot: `.`')
    )

    @property
    def converted_path(self):
        filepath = str(self.video.file) # fix it
        filepath = filepath.replace(FFMPEG_ORIG_VIDEO, FFMPEG_CONV_VIDEO)
        return re.sub(r'[^\.]{1,10}$', self.convert_extension, filepath)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')
