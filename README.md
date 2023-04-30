# Django ffmpeg

Download and re-encode video files by using `ffmpeg` utilit or any another command line tool.

Since **0.0.7** version support **Django 2** and above only.

## Authors

The original version is created by [Alrusdi](https://github.com/alrusdi/). Modify, making separate application, refactoring and further development [pixxxel](https://github.com/pixxxel/)

## Install

```shell
pip install django-ffmpeg
```

Optionally in `settings.py` set directories names (`FFMPEG_PRE_DIR`, `FFMPEG_ORIG_VIDEO`, `FFMPEG_THUMB_VIDEO`, `FFMPEG_CONV_VIDEO`) for video files. Structure in MEDIA_ROOT by default is:

```
media
  ├ ...
  └ videos
    ├ conv
    ├ orig
    └ thumb
```

Add `'django_ffmpeg'` to `INSTALLED_APPS` and execute `python manage.py migrate`

## Dependencies

You must have [Ffmpeg](https://ffmpeg.org/) (or any other) utilit for converting video.

Possible get it for Ubuntu as:

```shell
sudo add-apt-repository ppa:mc3man/trusty-media
sudo apt-get update
sudo apt-get install ffmpeg
```

For Windows you must [download](https://www.ffmpeg.org/download.html) it.

Obviously, Django must have.

## Usage

For converting video set the command(s) to `ConvertingCommand` model
for example:

```shell
>>> from django_ffmpeg.models import ConvertingCommand
>>> ConvertingCommand(
	match_by='name',
	match_regex='.*',
	command='ffmpeg -y -hide_banner -nostats -i %(input_file)s -threads 0 -xerror %(output_file)s',
	convert_extension='mp4',
	thumb_command='ffmpeg -hide_banner -nostats -i %(in_file)s -y -frames:v 1 -ss %(thumb_frame)s %(out_file)s'
).save()
```

or add fixture:

```shell
python manage.py loaddata django-ffmpeg-init
```

Fragments `%(input_file)s` and `%(output_file)s` in `command` is required.

Fragments `%(in_file)s` and `%(thumb_frame)s` in `thumb_command` is required.

Option `-xerror ` is required for except ffmpeg conversion error to convert_status.

After this you must run `python manage.py convert_videos` or set it to crontab. Command is convert only one unconverted video at time. So execute this command as many times as unconverted videos is it.

Now you may reference on `django_ffmpeg.Video` model from other or get it directly.

If you're using Celery, you may invoke task for convert concrete video:

```python
from django_ffmpeg.tasks import convert_video

convert_video.delay(command_id, video_id)
```

or for convert last uncoverted:

```python
from django_ffmpeg.tasks import convert_first_pending

convert_first_pending.delay()
```
