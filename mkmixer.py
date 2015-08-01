from globals import *
import os
import fileTools
import subliminal
import subtitles
import babelfish

class MkvMixer(object) :
	@classmethod
	def mixVideo(cls_, videoFilePath_, subFilePaths_) :
		LOGGER.info('Mixing video %s with subtitles:' % videoFilePath_)
		for subFilePath in subFilePaths_ :
			LOGGER.info('  %s' % subFilePath)
	
	@classmethod
	def mixAndMove(_cls, sourceDirPath_, destDirPath_) :
		LOGGER.info('*** START MIXING VIDEOS ***')
		if (os.path.isdir(sourceDirPath_)) :
			for dir, dirs, files in os.walk(sourceDirPath_) :
				localDir = dir[len(sourceDirPath_):]
				for fileName in files :
					fileExtension = os.path.splitext(fileName)[1]
					filePath = os.path.join(dir, fileName)

					if (fileExtension in VIDEO_EXTENSIONS) :
						# Scan video
						LOGGER.debug('Scanning video \'%s\'', filePath)
						video = subliminal.scan_video(filePath, False, True)
							
						# TEMP: if no embedded subtitles have been found, try to find associated sub files
						# This should be done in 'subliminal.scan_video', but... NO.
						# TODO: fork subliminal to fix the method 'scan_subtitle_languages'
						subFileLanguages = subtitles.scanSubtitleLanguages(filePath, SUB_EXTENSIONS)
						
						# If subs found, then move video
						hasSubFiles = babelfish.Language('eng') in subFileLanguages
						hasEmbeddedSub = babelfish.Language('eng') in video.subtitle_languages
						if hasEmbeddedSub :
							LOGGER.debug('%s has already embedded subtitles, skip mixing' % fileName)
							fileTools.transferFile(filePath, sourceDirPath_, destDirPath_)
						elif hasSubFiles :
							LOGGER.debug('Subtitles files found for %s', video.name)
							
							# Find all subtitles files
							subFiles = []
							for otherFileName in files :
								otherFileExtension = os.path.splitext(otherFileName)[1]
								if (not otherFileName == fileName and otherFileExtension in SUB_EXTENSIONS) :
									# Test if the subtitles have the same name as the movie
									otherFileRoot = os.path.splitext(otherFileName)[0]
									fileRoot = os.path.splitext(fileName)[0]
									if (otherFileRoot[:len(fileRoot)] == fileRoot) :
										# Move subtitles
										otherFilePath = os.path.join(dir, otherFileName)
										subFiles.append(otherFilePath)
							assert len(subFiles) > 0
							MkvMixer.mixVideo(filePath, subFiles)
							fileTools.transferFile(filePath, sourceDirPath_, destDirPath_)
							# TODO: remove this when mixing is done
							for subFilePath in subFiles :
								fileTools.transferFile(subFilePath, sourceDirPath_, destDirPath_)
						else :
							LOGGER.debug('%s has already embedded subtitles, skip mixing' % fileName)
		else :
			LOGGER.warning('\'%s\' does not refer to an existing path.', sourceDirPath_)