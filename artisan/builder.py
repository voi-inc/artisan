# stdlib
import os

# 3rd party
from jinja2 import Environment, FileSystemLoader
from premailer import transform


#
# Builder Class. The engine that builds and syncs assets
#
class Builder(object):

	#
	# Setup - Merge Options
	#
	def __init__(self, type, src, dest, creds=None):

		# Defaults / Options
		self.type = type
		self.src  = src
		self.dest = dest
		
		# Make sure we have creds for cloud push
		if type != 'local':
			if not creds: raise ValueError('Must provide credentials')
			self.creds = creds


		# Master & Child Templates
		self.master_tmpls = os.path.join(self.src, 'masters')
		self.message_tmpls = os.path.join(self.src, 'messages')

		# Setup jinja root path
		self.jinja = Environment(loader=FileSystemLoader(self.src))


	#
	# Build all masters and messages 
	#
	def build(self):
		self.build_masters()
		self.build_messages()


	#
	# Loop over all masters and sync media
	#
	def build_masters(self):
		for name in os.listdir(self.master_tmpls):
			self.sync(os.path.join(self.master_tmpls, name))


	#
	# Loop over all messages and build
	#
	def build_messages(self):
		for name in os.listdir(self.message_tmpls):
			message_path = os.path.join(self.message_tmpls, name)
			self.write_template(message_path)
			self.sync(message_path)


	#
	# Build one message
	#
	def build_message(self, path):
		self.build_masters()
		self.write_template(path)
		self.sync(path)


	#
	# Template and modify index.html inside of dir
	#
	def write_template(self, path):
		abs_path = os.path.join(path, 'index.html')
		rel_path = abs_path.replace(self.src, '')

		# template
		tmpl = self.jinja.get_template(rel_path)
		# move styles inline
		tmpl = transform(tmpl.render())

		# save
		file_path = self.dest + rel_path
		dir_path = os.path.split(file_path)[0]
		# create dir if it does not exist
		if not os.path.isdir(dir_path):
			os.makedirs(dir_path)
		# open and write
		file = open(file_path, 'w+')
		file.write(tmpl)


	# 
	# Sync images
	#
	def sync(self, path):
		# src img directory
		img_dir = os.path.join(path, 'images')
		# only relevent if images exist
		if os.path.isdir(img_dir):
			# if dev mode copy
			if (self.type == 'local'):
				return self.sync_local(img_dir)
			else:
				self.sync_cloud(img_dir)


	# 
	# Sync local
	#
	def sync_local(self, dir):
		print 'copy ' + dir


	# 
	# Sync cloud
	#
	def sync_cloud(self, dir):
		print 'cloud ' + dir
