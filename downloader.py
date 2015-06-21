from pytvdbapi import api
from KickassAPI import Search, CATEGORY, ORDER
from globals import _dbFilePath, _logger
import feedparser
import transmissionrpc
import database
import subliminal
import sqlite3
import guessit

_db = None
_serieToFind = 'entourage'

def formatSeasonEpisode(season_, episode_) :
	seasonEpisode = 's'
	if (season_ < 10) :
		seasonEpisode += '0'
	seasonEpisode +=  str(season_) + 'e'
	if (episode_ < 10) :
		seasonEpisode += '0'
	seasonEpisode += str(episode_)
	return seasonEpisode

def findSerieInfos(serieName_) :
	_db = api.TVDB("B43FF87DE395DF56")
	result = _db.search(serieName_, "en")
	if len(result) > 0 :
		return result[0]
	else :
		return None

def downloadSeasonFromKickass(serieName_, season_) :
	conn = sqlite3.connect(_dbFilePath)
	c = conn.cursor()
	
	serieInfo = findSerieInfos(serieName_);
	if not serieInfo is None and season_ < len(serieInfo) :
		for episode in range(1, len(serieInfo[season_])):
			localDbInfo = database.getEpisodeInfo(c, serieName_, season_, episode);
			if localDbInfo is None :
				downloadEpisodeFromKickass(serieName_, season_, episode)

	conn.close()
		
def downloadEpisodeFromKickass(serieName_, season_, episode_) :
	search = serieName_ + ' ' + formatSeasonEpisode(season_, episode_) + ' 720p'
	print "searching: " + search
	results = Search(search).category(CATEGORY.TV).order(ORDER.SEED)
	if (not results is None) :
		downloadFromMagnetLink(results.list()[0].magnet_link)

def downloadFromMagnetLink(link_) :	
	tc = transmissionrpc.Client('localhost', port=9091, user='s0ubap', password='4nt4r3s21!')
	torrent = tc.add_torrent(link_)

def downloadFromRSS() :
	_logger.info('*** START DOWNLOADING SUBTITLES ***')
	
	conn = sqlite3.connect(_dbFilePath)
	c = conn.cursor()
	
	feed = feedparser.parse('http://showrss.info/rss.php?user_id=244944&hd=null&proper=null')
	for item in feed['items'] :
		title = item['title']
		link = item['link']
		video = subliminal.Video.fromguess(title, guessit.guess_file_info(title))
		localDbInfo = database.getEpisodeInfo(c, video.series, video.season, video.episode);
		if ( localDbInfo is None ) :
			print 'downloading %s' % title
			downloadFromMagnetLink(link)
			database.updateEpisode(c, video, False, False, False)
		else :
			print 'Skip %s: already in database' % title
		
	conn.commit()
	conn.close()
	
def mainFunction() :
	#downloadSeasonFromKickass('halt and catch fire', 1)
	downloadFromRSS()

#mainFunction()