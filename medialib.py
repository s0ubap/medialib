from globals import _logger, _mediaPath, _seriesDir
import os
import fileTools
import subliminal
import subtitles
import babelfish
import downloader
from pytvdbapi import api

#===============================================================================
# Globals
#===============================================================================
_scanPath = ur'/home/s0ubap/torrent/completed/'
_tempPath = ur'/mnt_wd1/_mediatemp/'
_mediaPath = ur'/mnt_wd1/medias/'
_seriesDir = ur'shows/'
_moviesDir = ur'movies/'

_videoExtensions = ('.avi', '.mp4', '.mkv')
_subExtensions = ('.srt', '.sub')

#===============================================================================
#===============================================================================
def formatEpisodePath( episode_ ) :
	"""Format an episode name: Series - SxxExx - Title

	:param String episode_: episode path
	:return String: formatted episode path
	"""
	extension = os.path.splitext(episode_.name)[1]
	episodeFilePath = episode_.series + '/' + 'Season '
	if (episode_.season < 10) :
		episodeFilePath += '0'
	episodeFilePath +=  (str(episode_.season) + '/' + episode_.series + ' - S')
	if (episode_.season < 10) :
		episodeFilePath += '0'
	episodeFilePath += (str(episode_.season) + 'E')
	if (episode_.episode < 10) :
		episodeFilePath += '0'
	episodeFilePath += (str(episode_.episode) + ' - ' + episode_.title + extension)
	return episodeFilePath

#===============================================================================
#===============================================================================
def moveAndRenameMovie(movie_, destDirPath_, _ext) :		
	"""Move and rename an movie

	:param episode_: Movie to process.
	:type episode_: class subliminal.video.Movie.
	:param String destDirPath_: Path of the directory to move the Movie to.
	:param String _ext: Extension of the Movie file.
	"""

	# Check episode informations
	if ( episode_.title is None ) :
		_logger.error('No title found while trying to move and rename file: \'%s\'', movie_.name)
		return

#===============================================================================
#===============================================================================
def moveAndRenameEpisode(episode_, destDirPath_) :
	"""Move and rename an episode

	:param episode_: Episode to process.
	:type episode_: class subliminal.video.Episode.
	:param String destDirPath_: Path of the directory to move the episode to.
	"""
	
	# Check episode informations
	if ( episode_.title is None ) :
		_logger.error('No episode series title found while trying to move and rename file: \'%s\'', episode_.title)		
		return
	if ( episode_.series is None ) :
		_logger.error('No episode series name found while trying to move and rename file: \'%s\'', episode_.name)		
		return
	if ( episode_.episode is None ) :
		_logger.error('No episode number found while trying to move and rename file: \'%s\'', episode_.name)
		return
	if ( episode_.season is None ) :
		_logger.error('No episode season found while trying to move and rename file: \'%s\'', episode_.name)
		return

	episodeFilePath = os.path.join(os.path.join(destDirPath_, _seriesDir), formatEpisodePath(episode_))
	fileTools.moveFile(episode_.name, episodeFilePath)
	
#===============================================================================
#===============================================================================
def moveAndRenameDownloadedVideos(sourceDirPath_, destDirPath_) :
	"""Move all videos (movies and episodes) from the source path to the destination
	path, and rename them.

	:param String sourceDirPath_
	:param String destDirPath_
	"""

	_logger.info('*** START MOVING AND RENAMING DOWNLOADED VIDEOS ***')
	
	if (os.path.isdir(sourceDirPath_)) :
		# Parse all files
		for dir, dirs, files in os.walk(sourceDirPath_) :
			for fileName in files :
				# Retrieve paths
				fileExtension = os.path.splitext(fileName)[1]
				filePath = os.path.join(dir, fileName)
				
				if (fileExtension in _videoExtensions) :
					# Create video instance
					_logger.debug('Scanning video file \'%s\'', filePath)
					
					video = subliminal.scan_video(filePath, True, True)
					print video
					# Specific action according to the type of video
					if (not video is None) :
						if (isinstance(video, subliminal.video.Episode)) :
							if (video.title is None) :
								db = api.TVDB("B43FF87DE395DF56")
								result = db.search(video.series, "en")
								video.title  = unicode(result[0][video.season][video.episode].EpisodeName)
							moveAndRenameEpisode(video, destDirPath_);
						elif (isinstance(video, subliminal.video.Movie)) :
							moveAndRenameMovie(video, destDirPath_);
						else :
							_logger.info('Bad video type, skipping file. (%s)', filePath)
				else :
					_logger.info('Bad extension, skipping file. (%s)', filePath)
	else :
		_logger.warning('\'%s\' does not refer to an existing path.', sourceDirPath_)

#===============================================================================
#===============================================================================
def moveVideosAndSubtitles(sourceDirPath_, destDirPath_) :
	"""Move videos and subtitles (if exist)

	:param String sourceDirPath_
	:param String destDirPath_
	"""

	_logger.info('*** START MOVING VIDEOS AND SUBTITLES ***')
	
	if (os.path.isdir(sourceDirPath_)) :
		for dir, dirs, files in os.walk(sourceDirPath_) :
			localDir = dir[len(sourceDirPath_):]
			for fileName in files :
				fileExtension = os.path.splitext(fileName)[1]
				filePath = os.path.join(dir, fileName)

				if (fileExtension in _videoExtensions) :
					# Scan video
					_logger.debug('Scanning video \'%s\'', filePath)
					video = subliminal.scan_video(filePath, False, True)
						
					# TEMP: if no embedded subtitles have been found, try to find associated sub files
					# This should be done in 'subliminal.scan_video', but... NO.
					# TODO: fork subliminal to fix the method 'scan_subtitle_languages'
					subFileLanguages = subtitles.scanSubtitleLanguages(filePath, _subExtensions)
					
					# If subs found, then move video
					hasSubFiles = babelfish.Language('eng') in subFileLanguages
					hasEmbeddedSub = babelfish.Language('eng') in video.subtitle_languages or babelfish.Language('und') in video.subtitle_languages
					if (hasEmbeddedSub or hasSubFiles) :
						fileTools.transferFile(filePath, sourceDirPath_, destDirPath_)
						
						# Embedded subtitles?
						if (hasEmbeddedSub) :
							_logger.debug('Embedded subtitles found for %s', video.name)
					
						# If subtitles files have been found, then move
						if (hasSubFiles) :
							_logger.debug('Subtitles files found for %s', video.name)
							# Move subtitles
							for otherFileName in files :
								otherFileExtension = os.path.splitext(otherFileName)[1]
								if (not otherFileName == fileName and otherFileExtension in _subExtensions) :
									# Test if the subtitles have the same name as the movie
									otherFileRoot = os.path.splitext(otherFileName)[0]
									fileRoot = os.path.splitext(fileName)[0]
									if (otherFileRoot[:len(fileRoot)] == fileRoot) :
										# Move subtitles
										otherFilePath = os.path.join(dir, otherFileName)
										fileTools.transferFile(otherFilePath, sourceDirPath_, destDirPath_)
					else :
						_logger.warning('No subtitles found, skipping video. (%s)', video.name)
				
	else :
		_logger.warning('\'%s\' does not refer to an existing path.', sourceDirPath_)


#===============================================================================
#===============================================================================
def mainFunction() :
	# Download series
	#downloader.mainFunction()

	# Rename and move downloaded videos in a temp folder
	moveAndRenameDownloadedVideos(_scanPath, _tempPath)
	
	# Download subtitles
	subtitles.downloadSubtitles(_tempPath)
	
	# Move videos and their subtitles in the final folder
	moveVideosAndSubtitles(_tempPath, _mediaPath)
	
	# Delete empty directories
	fileTools.deleteEmptyDirectories(os.path.join(_tempPath, _seriesDir), False)
	
mainFunction()