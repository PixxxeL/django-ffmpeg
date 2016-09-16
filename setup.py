from distutils.core import setup
import django_ffmpeg

setup(
    name = "django-ffmpeg",
    version = django_ffmpeg.__version__,
    packages = ["django_ffmpeg"],
    url = 'https://github.com/PixxxeL/django-ffmpeg',
    author = 'pixel',
    author_email = 'ivan.n.sergeev@gmail.com',
    maintainer = 'pixel',
    maintainer_email = 'ivan.n.sergeev@gmail.com',
    license = 'GPL3',
    description = 'Download and encode video files by using ffmpeg utilit',
    download_url = 'https://github.com/PixxxeL/django-ffmpeg/archive/master.zip',
    classifiers = [
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    package_data = {
        'django_ffmpeg': [
            'locale/*/LC_MESSAGES/*',
            'management/*.py',
            'management/commands/*.py',
            'migrations/*.py',
        ],
    },
    include_package_data = True,
)
