# Django ffmpeg

Download and encode video files by using `ffmpeg` utilit or any another (?) command line tool.

## Authors

The original version is created by [Alrusdi](https://github.com/alrusdi/).
Modify, making separate application, refactoring and further development [pixxxel](https://github.com/pixxxel/)

## Install

```shell
pip install django-ffmpeg
```

Create structure in MEDIA_ROOT directory:

```
videos
  |- orig
  |- thumb
  |- conv
```
or set another existing directory names by `FFMPEG_PRE_DIR`, `FFMPEG_ORIG_VIDEO`,
`FFMPEG_THUMB_VIDEO`, `FFMPEG_CONV_VIDEO` in `settings.py`.

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
>>> ConvertingCommand(match_by='name', match_regex='.*', command='/usr/bin/ffmpeg -hide_banner -nostats -i %(input_file)s -target film-dvd %(output_file)s', convert_extension='mp4').save()
```

Fragments `%(input_file)s` and `%(output_file)s` in `command` is required.

After this you must run `python manage.py convert_videos` or set it to crontab.
Command convert one unprocessed video at time.
So execute this command as many times as video is.

Now you may reference on `django_ffmpeg.Video` model from other or get it directly.

## Todo
* Converting output is lose
* Add converting error output to `last_convert_msg`
* Refactoring thumbnail command
