# stdlib
import os
import subprocess

# 3rd party
from jinja2 import Environment, FileSystemLoader
from premailer import transform


class Artisan(object):

	#
	# Setup - Merge Options
	#
	def __init__(self, env='dev', cwd=os.getcwd(), port=8080, outDir='dev', srcDir='src'):

		# Defaults / Options
		self.env    = env
		self.cwd    = cwd
		self.port   = port
		self.outDir = os.path.join(self.cwd, outDir)
		self.srcDir = os.path.join(self.cwd, srcDir)

		# Master & Child Templates
		self.mTmpls = os.path.join(self.srcDir, 'masters')
		self.cTmpls = os.path.join(self.srcDir, 'messages')

		# Setup jinja root path
		self.jinja = Environment(loader=FileSystemLoader(self.srcDir))


	#
	# Build all masters and messages 
	#
	def build(self):
		self.buildMasters()
		self.buildMessages()


	#
	# Loop over all masters and sync media
	#
	def buildMasters(self):
		for name in os.listdir(self.mTmpls):
			self.sync(os.path.join(self.mTmpls, name))


	#
	# Loop over all messages and build
	#
	def buildMessages(self):
		for name in os.listdir(self.cTmpls):
			messagePath = os.path.join(self.cTmpls, name)
			self.writeTemplate(messagePath)
			self.sync(messagePath)


	#
	# Build one message
	#
	def buildMessage(self, path):
		self.buildMasters()
		self.writeTemplate(path)
		self.sync(path)


	#
	# Template and modify index.html inside of dir
	#
	def writeTemplate(self, path):
		absPath = os.path.join(path, 'index.html')
		relPath = absPath.replace(self.srcDir, '')

		# template
		tmpl = self.jinja.get_template(relPath)
		# move styles inline
		tmpl = transform(tmpl.render())

		# save
		filePath = self.outDir + relPath
		dirPath = os.path.split(filePath)[0]
		# create dir if it does not exist
		if not os.path.isdir(dirPath):
			os.makedirs(dirPath)
		# open and write
		file = open(filePath, 'w+')
		file.write(tmpl)


	# 
	# Sync images
	#
	def sync(self, path):
		# src img directory
		imgDir = os.path.join(path, 'images')
		# only relevent if images exist
		if os.path.isdir(imgDir):
			# if dev mode copy
			if (self.env == 'dev'):
				print 'copy'
			# else must be prod - sync with s3 
			else:
				print 'cloud time'


	#
	# Serve files for quick preview
	#
	def serve(self):
		# Change to cur Dir
		cachedCwd = os.getcwd()
		os.chdir(os.path.split(os.path.realpath(__file__))[0])

		# Start server
		self.process = subprocess.Popen(['python', '-u', 'server.py', '-d', self.outDir], stdout=subprocess.PIPE)
		while self.process.poll() is None: 
			if self.process.stdout.readline():
				break

		# Reset back to original cwd
		os.chdir(cachedCwd)