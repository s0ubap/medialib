from globals import _simulateMode
from globals import _logger
import os
import logging
import shutil

#===============================================================================
#===============================================================================
def testFileExtension(filePath_, extensions_) :
	assert os.path.exists(filePath_)
	fileName, fileExtension = os.path.splitext(filePath_)
	return (fileExtension in extensions_)
	
#===============================================================================
#===============================================================================
def moveFile(srcFilePath_, destFilePath_) :
	_logger.info('Moving file:');
	_logger.info('  From: %s', srcFilePath_)
	_logger.info('  To: %s', destFilePath_)
	
	if _simulateMode :
		return
	
	if (not os.path.isdir(os.path.dirname(destFilePath_))) :
		os.makedirs(os.path.dirname(destFilePath_))
	#os.rename(srcFilePath_, destFilePath_)
	shutil.move(srcFilePath_, destFilePath_)

#===============================================================================
#===============================================================================
def deleteEmptyDirectories(path_, deletePath_) :
	dirList = os.listdir(path_)
	for dir in dirList :
		dirPath = os.path.join(path_, dir)
		if ( os.path.isdir(dirPath) ) :
			deleteEmptyDirectories(dirPath, True)
	
	if deletePath_ :
		dirList = os.listdir(path_)
		if (len(dirList) == 0) :
			_logger.info('Deleting empty directory: %s', path_)
			if not _simulateMode :
				os.rmdir(path_)
		
#===============================================================================
#===============================================================================
def transferFile(filePath_, srcRootPath_, destDirPath_) :
	assert filePath_.startswith( srcRootPath_ )
	localFilePath = filePath_[len(srcRootPath_):]
	destFilePath = os.path.join(destDirPath_, localFilePath)
	
	moveFile(filePath_, destFilePath)