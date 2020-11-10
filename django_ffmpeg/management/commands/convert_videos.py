import logging
import time

from django.core.management.base import BaseCommand

from django_ffmpeg.utils import Converter


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    args = 'no arguments'
    help = 'Converts unconverted video'

    def handle(self, *args, **options):
        start = time.time()
        Converter().convert_first_pending()
        logger.info('Job finished at: %s s' % (time.time() - start))
