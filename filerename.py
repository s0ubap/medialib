from pytvdbapi import api
from globals import *
from video import EpisodeInfo, VideoInfo
import os
import fileTools
from subdownload import SubDownloader
from mkmixer import MkvMixer
import database
import downloader

class VideoRename(object) :
	def __init__(self, sourceDirPath_, destDirPath_) :
		self.sourceDirPath = sourceDirPath_
		self.destDirPath = destDirPath_
		self.tvdb = api.TVDB("B43FF87DE395DF56")

	def renameEpisode(self, filePath_, episodeInfo_) :
		extension = os.path.splitext(filePath_)[1]
		episodeFilePath = os.path.join(os.path.join(self.destDirPath, SERIES_DIR), episodeInfo_.formatEpisodeFilePath(extension))
		fileTools.moveFile(filePath_, episodeFilePath)		

	def renameAll(self) :
		LOGGER.info('***RENAMING DOWNLOADED VIDEOS ***')
		
		if (os.path.isdir(self.sourceDirPath)) :
			# Parse all files
			for dir, dirs, files in os.walk(self.sourceDirPath) :
				for fileName in files :
					# Retrieve paths
					fileExtension = os.path.splitext(fileName)[1]
					filePath = os.path.join(dir, fileName)
				
					if (fileExtension in VIDEO_EXTENSIONS) :
						# Create video instance
						LOGGER.debug('Scanning video file \'%s\'', filePath)
						
						# Create a video info
						videoInfo = None
						try :
							videoInfo = VideoInfo.fromFileName(fileName, self.tvdb)
						except RuntimeError, e :
							LOGGER.info('Skipping %s: %s', fileName, str(e))
						except ValueError, e :
							LOGGER.info('Skipping %s: %s', fileName, str(e))

						# Specific action according to the type of video
						if (not videoInfo is None) :
							if (isinstance(videoInfo, EpisodeInfo)) :								
								# Rename the episode
								LOGGER.info('Rename episode: %s' % fileName)
								self.renameEpisode(filePath, videoInfo);
					else :
						LOGGER.info('Bad extension, skipping file. (%s)', filePath)
		else :
			LOGGER.warning('\'%s\' does not refer to an existing path.', self.sourceDirPath)

def mainFunction() :
	#database.createDB(DB_FILE_PATH)
	#database.updateSeriesDB(DB_FILE_PATH, MEDIA_PATH + SERIES_DIR)
	
	downloader.downloadFromRSS()
	
	for path in SCAN_PATH :
		videoRename = VideoRename(path, TEMP_PATH)
		videoRename.renameAll()
	
	subDownloader = SubDownloader(TEMP_PATH)
	subDownloader.downloadsubtitles()
	
	MkvMixer.mixAndMove(TEMP_PATH+SERIES_DIR, MEDIA_PATH+SERIES_DIR)
	
mainFunction()