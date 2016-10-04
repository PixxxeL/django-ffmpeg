# -*- coding: utf-8 -*-

import os
import re
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from django_ffmpeg.defaults import *


def filename_normalize(filename):
    ext = filename.split('.')[-1]
    return '%s.%s' % (uuid4().hex, ext)


def video_file_path(instance, filename):
    return '%s/%s/%s' % (FFMPEG_PRE_DIR, FFMPEG_ORIG_VIDEO, filename_normalize(filename),)


def thumb_file_path(instance, filename):
    return '%s/%s/%s' % (FFMPEG_PRE_DIR, FFMPEG_THUMB_VIDEO, filename_normalize(filename),)


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
        help_text = 'Example: /usr/bin/ffmpeg -nostats -y -i %(input_file)s -acodec libmp3lame -ar 44100 -f flv %(output_file)s',
    )
    convert_extension = models.CharField(
        max_length=5,
        verbose_name=_('Extension'),
        help_text = _('Without dot: `.`'),
    )
    thumb_command = models.TextField(
        verbose_name=_('System command to convert thumb'),
        help_text = 'Example: /usr/bin/ffmpeg -hide_banner -nostats -i %(in_file)s -y -frames:v 1 -ss %(thumb_frame)s %(out_file)s',
    )

    def __unicode__(self):
        return self.command[0:50]

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
        upload_to=video_file_path,
    )
    thumb = models.ImageField(
        verbose_name=_('Thumbnail image'),
        upload_to=thumb_file_path,
        null=True, blank=True,
    )
    thumb_frame = models.PositiveIntegerField(
        verbose_name=_('Frame number for thumbnail'),
        default=0,
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
        help_text = _('Without dot: `.`'),
        null=True, editable=False,
    )

    @property
    def converted_path(self):
        if not self.convert_extension:
            return None
        filepath = self.video.path
        filepath = filepath.replace(FFMPEG_ORIG_VIDEO, FFMPEG_CONV_VIDEO)
        return re.sub(r'[^\.]{1,10}$', self.convert_extension, filepath)

    @property
    def thumb_video_path(self):
        filepath = self.video.path
        filepath = filepath.replace(FFMPEG_ORIG_VIDEO, FFMPEG_THUMB_VIDEO)
        return re.sub(r'[^\.]{1,10}$', 'jpg', filepath)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')
