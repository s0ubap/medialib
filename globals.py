import logging

#===============================================================================
# _loggers
#===============================================================================
LOGGER = logging.getLogger("medialib")
LOGGER.setLevel(logging.DEBUG)
_handler = logging.StreamHandler()
_handler.setLevel(logging.DEBUG)
LOGGER.addHandler(_handler)

SUBLIMINAL_LOGGER = logging.getLogger('subliminal')
SUBLIMINAL_LOGGER.setLevel(logging.DEBUG)
_subliminalHandler = logging.StreamHandler()
_subliminalHandler.setLevel(logging.WARNING)
SUBLIMINAL_LOGGER.addHandler(_subliminalHandler)

#===============================================================================
# Globals
#===============================================================================
SIMULATE_MODE = False
DB_FILE_PATH = ur'/mnt_wd1/medias/medialib.db'
#SCAN_PATH = ur'/home/s0ubap/torrent/completed/'
SCAN_PATH = (ur'/mnt_wd1/torrent_completed/', ur'/home/s0ubap/torrent/completed/')
TEMP_PATH = ur'/mnt_wd1/_mediatemp/'
MEDIA_PATH = ur'/mnt_wd1/medias/'
SERIES_DIR = ur'shows/'
MOVIE_DIR = ur'movies/'

VIDEO_EXTENSIONS = ('.avi', '.mp4', '.mkv')
SUB_EXTENSIONS = ('.srt', '.sub')