import logging

#===============================================================================
# Loggers
#===============================================================================
_logger = logging.getLogger("medialib")
_logger.setLevel(logging.DEBUG)
_handler = logging.StreamHandler()
_handler.setLevel(logging.INFO)
_logger.addHandler(_handler)

_subliminalLogger = logging.getLogger('subliminal')
_subliminalLogger.setLevel(logging.DEBUG)
_subliminalHandler = logging.StreamHandler()
_subliminalHandler.setLevel(logging.INFO)
_subliminalLogger.addHandler(_subliminalHandler)

#===============================================================================
# Globals
#===============================================================================
_simulateMode = False
_dbFilePath = ur'/mnt_wd1/medias/medialib.db'
_mediaPath = ur'/mnt_wd1/medias/'
_seriesDir = ur'shows/'