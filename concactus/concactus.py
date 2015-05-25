#!/usr/bin/env python
"""concactus.py
A python based preprocessor for HTML imports. 
Simple solution for importing common HTML on multiple pages!
"""
__author__ = "Jesse Qin"
__copyright__ = "Copyright 2015, Jesse Qin"
__credits__ = ["Jesse Qin"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Jesse Qin"
__email__ = "jesseqin@gmail.com"
__status__ = "Production"


import os
import glob
import re

cactusConfigFile = "concactus.ini"
cactusConfig = {}
cactusImports = {}
cactusIgnore = 'IGNORE_TRUE'
importStrL = "<!-- @concactus import: "
importStrR = "-->"
endStr = "<!-- @concactus end -->"

def loadCactus(iniFile):
	"""Loads config file and HTML import modules"""
	global cactusConfig, cactusImports
	#load everything in cactusConfigFile
	cactusConfig = dict(line.split(": ",1) for line in open(iniFile).read().splitlines() if len(line) > 1)

	#load importable html modules
	importPath = cactusConfig['importPath']
	for filename in glob.glob(os.path.join(importPath, '*.html')):
			cactusImports[os.path.basename(filename)] = open(filename).read().splitlines();


def executeImports():
	"""Go through all files in input path"""
	global cactusConfig
	inputPath = cactusConfig['inputPath']
	outputPath = cactusConfig['outputPath']

	#find all html files in input path
	for filename in glob.glob(os.path.join(inputPath, '*.html')):
		if os.path.basename(filename) not in cactusConfig:
			importIntoFile(filename, outputPath + os.path.basename(filename))


def importIntoFile(filename, outputFile):
	"""Import into an individual file"""
	#grab contents of current file
	currFile = open(filename).read().splitlines()

	#export file
	wFile = open(outputFile, 'w+')

	print "\tImporting into " + outputFile + ":\n\t\t",

	#parse and write
	skipWrite = False
	spaceAppend = ""
	for line in currFile:
		if line.find(importStrL) != -1:
			skipWrite = True
			wFile.write(line)
			#handling indentation and space consistency
			spaceAppend = re.match(r"\s+", line).group()
			line = line.replace(importStrL, "").replace(importStrR, "").strip()
			wFile.write('\n')
			#import lines, matching indentation
			for importLine in cactusImports[line]:
				wFile.write(spaceAppend + importLine + '\n')
			print line,
		else:
			if line.find(endStr) != -1:
				skipWrite = False
			if not skipWrite:
				wFile.write(line+'\n')
	print '\n'
	wFile.close()

if __name__ == "__main__":
	"""Main Driver"""
	loadCactus(cactusConfigFile)
	executeImports()


