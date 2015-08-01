from pytvdbapi import api
import guessit
import sqlite3
import subliminal

class VideoInfo(object) :
	@classmethod
	def fromFileName(cls, fileName_, tvdb_ = None) :
		guess = guessit.guess_file_info(fileName_)
		try:
			if guess['type'] == 'episode' :
				return EpisodeInfo.fromFileName(guess, fileName_, tvdb_)
			elif guess['type'] != 'movie' :
				raise ValueError('The file name must refer to an episode or a movie')
		except:
			raise

class EpisodeInfo(VideoInfo) :
	def __init__(self, name_, title_, season_, episode_) :
		self.name = name_
		self.title = title_
		self.season = season_
		self.episode = episode_
	
	@classmethod
	def fromEpisode(cls, seriesName_, season_, episode_, tvdb_) :
			# Retrieve name and title from guess using tvdb
			result = tvdb_.search(guess['series'], "en")		
			if result is None or len(result) <= 0 :
				raise RuntimeError('No data found in tvdb for %s', guess['series'])
			show = result[0]
			return cls(show.SeriesName, show[season_][episode_].EpisodeName, season_, episode_)
			
	@classmethod
	def fromFileName(cls, guess_, fileName_, tvdb_ = None) :
		if guess_['type'] != 'episode' :
			raise ValueError('The guess must be a episode')
		
		if 'series' not in guess_ :
			raise ValueError('Insufficient data: could not guess series name')
		if 'season' not in guess_ :
			raise ValueError('Insufficient data: could not guess episode season')
		if 'episodeNumber' not in guess_ :
			raise ValueError('Insufficient data: could not guess episode number')
		
		season = guess_['season']
		episodeNumber = guess_['episodeNumber']
		if (tvdb_ is None) :
			# no tvdb, create video only from guess
			title = guess_.get('title')
			if title is None :
				raise ValueError('Insufficient data: could not guess episode title')
			return cls(guess_['series'], title, season, episodeNumber)
		else :
			# Retrieve name and title from guess using tvdb
			result = tvdb_.search(guess_['series'], "en")
			if result is None or len(result) <= 0 :
				raise RuntimeError('No data found in tvdb for %s' % guess_['series'])
			show = result[0]
			return cls(show.SeriesName, show[season][episodeNumber].EpisodeName, season, episodeNumber)

	@classmethod
	def updateSubliminalEpisodeInfo(cls, subliminalEpisode) :
		info = cls.fromEpisode(subliminalEpisode.series, subliminalEpisode.season, subliminalEpisode.episode)
		subliminalEpisode.series = info.name
		subliminalEpisode.title = info.title
	
	def formatEpisodeFilePath(self, extension_) :
		episodeFilePath = self.name + '/' + 'Season '
		if (self.season < 10) :
			episodeFilePath += '0'
		episodeFilePath +=  (str(self.season) + '/' + self.name + ' - S')
		if (self.season < 10) :
			episodeFilePath += '0'
		episodeFilePath += (str(self.season) + 'E')
		if (self.episode < 10) :
			episodeFilePath += '0'
		episodeFilePath += (str(self.episode) + ' - ' + self.title + extension_)
		return episodeFilePath
	