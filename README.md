# Django ffmpeg
Download and encode video files by using ffmpeg utilit

## Authors

The original version is created by [Alrusdi](https://github.com/alrusdi/).
Making separate application, refactoring and further development [pixxxel](https://github.com/pixxxel/)

## Dependencies

You must have [Ffmpeg](https://ffmpeg.org/) utilit for convert video.
Possible get it for Ubuntu as:
```shell
sudo add-apt-repository ppa:mc3man/trusty-media
sudo apt-get update
sudo apt-get dist-upgrade
sudo apt-get install ffmpeg
```

Obviously, Django must have.

Create structure in MEDIA_ROOT directory:
```
videos
  |- orig
  |- thumb
  |- conv
```
or set another directory names by `FFMPEG_PRE_DIR`, `FFMPEG_ORIG_VIDEO`,
`FFMPEG_THUMB_VIDEO`, `FFMPEG_CONV_VIDEO` in `settings.py`

## Usage

Ubuntu install:
```shell
pip install django-ffmpeg
```

You may reference on `django_ffmpeg.Video`

## Todo
*
