from pytvdbapi import api
from KickassAPI import Search

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

def downloadEpisode(serieName_, season_, episode_) :
	search = serieName_ + ' ' + formatSeasonEpisode(season_, episode_) + ' 720p'
	print "searching: " + search
	for t in Search("Game of thrones"):
		t.lookup()
		
def mainFunction() :
	downloadEpisode('Silicon valley', 1, 1)

mainFunction()