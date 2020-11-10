from celery.task import task

from django_ffmpeg.models import Video, ConvertingCommand
from django_ffmpeg.utils import Converter


@task
def convert_video(command_id, video_id):
    command = ConvertingCommand.objects.get(pk=command_id)
    video = Video.objects.get(pk=video_id)
    converter = Converter()
    converter.convert_video_thumb(command, video)
    converter.convert_video_file(command, video)
