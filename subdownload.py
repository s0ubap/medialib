from globals import *
import os
import subliminal
import babelfish

class SubDownloader(object) :
	def __init__(self_, cacheDirPath_) :
		# configure the cache
		if (not os.path.isdir(cacheDirPath_)) :
			os.makedirs(cacheDirPath_)
		subliminal.region.configure('dogpile.cache.dbm', arguments={'filename': cacheDirPath_ + 'cachefile.dbm'})

		self_.scanPath = unicode(cacheDirPath_);
		
	def downloadsubtitles(self_) :
		LOGGER.info('*** START DOWNLOADING SUBTITLES ***')
		
		if SIMULATE_MODE :
			 return
		
		# scan for videos in the folder and their subtitles
		videos = subliminal.scan_videos(self_.scanPath, subtitles=True, embedded_subtitles=True)
	
		# download
		subs = subliminal.download_best_subtitles(videos, {babelfish.Language('eng')})
		
		# save
		for video, sub in subs.items():
			subliminal.save_subtitles(video, sub)