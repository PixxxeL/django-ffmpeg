# Django ffmpeg
Download and encode video files by using ffmpeg utilit

## Authors

The original version is created by [Alrusdi](https://github.com/alrusdi/).
Modify, making separate application, refactoring and further development [pixxxel](https://github.com/pixxxel/)

## Install

Ubuntu install:
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
or set another directory names by `FFMPEG_PRE_DIR`, `FFMPEG_ORIG_VIDEO`,
`FFMPEG_THUMB_VIDEO`, `FFMPEG_CONV_VIDEO` in `settings.py`

Set `FFMPEG_CONVERTER` to path of the converter or use default `/usr/bin/ffmpeg`

## Dependencies

You must have [Ffmpeg](https://ffmpeg.org/) utilit for convert video.
Possible get it for Ubuntu as:
```shell
sudo add-apt-repository ppa:mc3man/trusty-media
sudo apt-get update
sudo apt-get install ffmpeg
```

Obviously, Django must have.

## Usage

You may reference on `django_ffmpeg.Video` model from other

## Todo
*
