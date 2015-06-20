import sqlite3
import os
import subliminal
import logging
import babelfish

_db = ur'/mnt_wd1/medias/medialib.db'
_seriesPath = ur'/mnt_wd1/medias/shows/'

_subliminalLogger = logging.getLogger('subliminal')
_subliminalLogger.setLevel(logging.DEBUG)
_subliminalHandler = logging.StreamHandler()
_subliminalHandler.setLevel(logging.DEBUG)
_subliminalLogger.addHandler(_subliminalHandler)

def createDB(dbFilePath_) :
	if os.path.isfile(dbFilePath_) :
		os.remove(dbFilePath_)

	conn = sqlite3.connect(dbFilePath_)
	c = conn.cursor()
	
	
	command = """create table series (id INTEGER PRIMARY KEY,
				name VARCHAR(50),
				title VARCHAR(255),
				season INTEGER,
				episode INTEGER,
				sub_en INTEGER,
				sub_fr INTEGER)"""
	print command
	c.execute(command)
	conn.close()

def updateSeriesDB(dbFilePath_, seriesPath_) :
	conn = sqlite3.connect(dbFilePath_)
	c = conn.cursor()
	
	"""command = 'INSERT INTO series VALUES(?, ?, ?, ?, ?, ?, ?)' , ('null', 'test', 'test', 1, 2, 1, 1)
	print command
	c.execute(command)"""
	
	print "scan videos in %s" %seriesPath_
	videos = subliminal.scan_videos([seriesPath_], True, True)
	
	for video in videos :
		sub_en = 0
		sub_fr = 0
		if (babelfish.Language('eng') in video.subtitle_languages) :
			sub_en = 1
		if (babelfish.Language('fra') in video.subtitle_languages) :
			sub_fr = 1

		command = 'INSERT INTO series VALUES(?, ?, ?, ?, ?, ?, ?)' , ('null', video.series, video.title, str(video.season), str(video.episode), str(sub_en), str(sub_fr))
		print command
		c.execute('INSERT INTO series VALUES(null, ?, ?, ?, ?, ?, ?)' , (video.series, video.title, str(video.season), str(video.episode), str(sub_en), str(sub_fr)))
		
	conn.commit()
	conn.close()
	

def mainFunction() :
	createDB(_db)
	updateSeriesDB(_db, _seriesPath)
	
mainFunction()
	
#SELECT hints FROM media_items
#SELECT hints FROM media_items WHERE library_section_id=3;