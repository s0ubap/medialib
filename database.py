from globals import LOGGER, MEDIA_PATH, SERIES_DIR, DB_FILE_PATH
import sqlite3
import os
import subliminal
import logging
import babelfish
	
class DatabaseEpisodeInfo:
	id = None
	name = None
	title = None
	season = None
	episode = None
	subEn = None
	subFr = None
	downloading = None
	
#===============================================================================
#===============================================================================
def createDB(dbFilePath_) :
	"""Create table in the given database file
	
	:param String dbFilePath_: file path of the database file
	"""
	if os.path.isfile(dbFilePath_) :
		return
		#os.remove(dbFilePath_)

	LOGGER.info('Creating database file: %s', dbFilePath_)
	command = """create table series (id INTEGER PRIMARY KEY,
				name VARCHAR(50),
				title VARCHAR(255),
				season INTEGER,
				episode INTEGER,
				sub_en INTEGER,
				sub_fr INTEGER,
				downloading INTEGER)"""
	LOGGER.debug(command)
		
	conn = sqlite3.connect(dbFilePath_)
	c = conn.cursor()
	c.execute(command)
	conn.close()

#===============================================================================
#===============================================================================
def updateSeriesDB(dbFilePath_, seriesPath_) :
	"""Update the database for a given path
	
	:param String dbFilePath_
	:param String seriesPath_
	"""
	conn = sqlite3.connect(dbFilePath_)
	c = conn.cursor()
	
	LOGGER.info('*** START UPDATING DATABASE ***')
	videos = subliminal.scan_videos(seriesPath_, True, True)
	
	for video in videos :
		subEn = babelfish.Language('eng') in video.subtitle_languages
		subFr = babelfish.Language('fra') in video.subtitle_languages
		updateEpisode(c, video, subEn, subFr, True)
		
	conn.commit()
	conn.close()
	
#===============================================================================
#===============================================================================
def updateEpisode(cursor_, video_, subEng_, subFr_, downloading) :
	"""Update the database for a specific episode
	
	:param cursor_: sqlite3 cursor
	:param video_: video to update in database
	:param bool subEng_: is there an associated english sub for this episode
	:param bool subFr_: is there an associated french sub for this episode
	:param bool downloading: is this episode currently downloading
	"""
	LOGGER.info('Updating database for %s', video_.name)
	
	command = 'SELECT id FROM series WHERE name=\'%s\' AND season=%d AND episode=%d' % (video_.series, video_.season, video_.episode)
	cursor_.execute(command)
	row = cursor_.fetchone()
	foundId = row[0] if not row is None else None
	cursor_.execute('INSERT OR REPLACE INTO series (id, name, title, season, episode, sub_en, sub_fr, downloading) VALUES(?, ?, ?, ?, ?, ?, ?, 0)', (foundId, video_.series, video_.title, video_.season, str(video_.episode), str(int(subEng_)), str(int(subFr_))))
	
#===============================================================================
#===============================================================================
def getEpisodeInfo(cursor_, serie_, season_, episode_) :
	command = 'SELECT * FROM series WHERE name=\'%s\' AND season=%d AND episode=%d' % (serie_, season_, episode_)
	cursor_.execute(command)
	row = cursor_.fetchone()
	
	if row is None :
		return None
	
	info = DatabaseEpisodeInfo()
	info.id			    = int(row[0])
	info.name		    = row[1]
	info.title		    = row[2]
	info.season		    = int(row[3])
	info.episode	    = int(row[4])
	info.subEn		    = bool(row[5])
	info.subFr		    = bool(row[6])
	info.downloading    = bool(row[7])
	return info;
	
#===============================================================================
#===============================================================================
def mainFunction() :
	createDB(DB_FILE_PATH)
	#updateSeriesDB(DB_FILE_PATH, ur'/mnt_wd1/medias/shows/Bored to Death/Season 01')
	updateSeriesDB(DB_FILE_PATH, MEDIA_PATH + SERIES_DIR)
	
#mainFunction()