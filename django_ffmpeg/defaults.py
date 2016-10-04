from django.conf import settings

FFMPEG_PRE_DIR     = getattr(settings, 'FFMPEG_PRE_DIR',     'videos')
FFMPEG_ORIG_VIDEO  = getattr(settings, 'FFMPEG_ORIG_VIDEO',  'orig')
FFMPEG_THUMB_VIDEO = getattr(settings, 'FFMPEG_THUMB_VIDEO', 'thumb')
FFMPEG_CONV_VIDEO  = getattr(settings, 'FFMPEG_CONV_VIDEO',  'conv')
FFMPEG_LOGGING_FILE_PATH = getattr(settings, 'FFMPEG_LOGGING_FILE_PATH',  None)
