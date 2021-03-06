from globals import SIMULATE_MODE
from globals import LOGGER
import os
import subliminal
import babelfish

_cachePath = '/home/s0ubap/medialib/_cache/'

#===============================================================================
#===============================================================================
def downloadSubtitles(path_) :
	"""Download all subtitles in the given path

	:param String path_
	"""
	
	LOGGER.info('*** START DOWNLOADING SUBTITLES ***')

	if SIMULATE_MODE :
		return
	
	# configure the cache
	if (not os.path.isdir(_cachePath)) :
		os.makedirs(_cachePath)
	subliminal.cache_region.configure('dogpile.cache.dbm', arguments={'filename': _cachePath + 'cachefile.dbm'})
	
	# scan for videos in the folder and their subtitles
	upath = unicode(path_)
	videos = subliminal.scan_videos(upath, subtitles=True, embedded_subtitles=True)
	
	# download
	subs = subliminal.download_best_subtitles(videos, {babelfish.Language('eng')})

#===============================================================================
#===============================================================================
def scanSubtitleLanguages(videoPath_, subExtensions_) :
	"""Search for subtitles with alpha2 extension from a video `path` and return their language
	:param string path: path to the video
	:return: found subtitle languages
	:rtype: set
	"""
	
	language_extensions = tuple('.' + c for c in babelfish.language_converters['alpha2'].codes)
	dirpath, filename = os.path.split(videoPath_)
	subtitles = set()
	for p in os.listdir(dirpath):
		if p.startswith(os.path.splitext(filename)[0]) and p.endswith(subExtensions_):
			if os.path.splitext(p)[0].endswith(language_extensions):
				subtitles.add(babelfish.Language.fromalpha2(os.path.splitext(p)[0][-2:]))
			else:
				subtitles.add(babelfish.Language('und'))
	return subtitles


