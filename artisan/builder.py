# stdlib
import os
import time
import shutil
import boto

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
	def __init__(self, type, src, dest, aws=None):

		# Defaults / Options
		self.type = type
		self.src  = src
		self.dest = dest
		
		# Make sure we have creds for cloud push
		if type != 'local':
			if not aws: raise ValueError('Must provide credentials')
			self.aws = aws


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
		if (self.type == 'local'):
			tmpl = transform(tmpl.render())
		else:
			base_url = 'https://s3.amazonaws.com/' + self.aws['bucket']
			tmpl = transform(tmpl.render(), base_url=base_url)
		

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
			if (self.type == 'local'):
				return self.sync_local(img_dir)
			else:
				self.sync_cloud(img_dir)


	# 
	# Sync local
	#
	def sync_local(self, dir):
		dest = dir.replace(self.src, self.dest)
		shutil.copytree(dir, dest)


	# 
	# Sync cloud
	#
	def sync_cloud(self, dir):
		conn = boto.connect_s3(
			aws_access_key_id=self.aws['aws_access_key_id'],
			aws_secret_access_key=self.aws['aws_secret_access_key'])

		# delete bucket if it exists
		bucket = conn.lookup(self.aws['bucket'])
		if bucket is not None:
			# delete keys
			for key in bucket.list():
				key.delete()
			# delete bucket
			conn.delete_bucket(self.aws['bucket'])
		
		# create bucket
		bucket = conn.create_bucket(self.aws['bucket'])

		# add all images & make public
		for name in os.listdir(dir):
			file_name = os.path.join(dir, name)
			key_name = os.path.join(dir.replace(self.src, ''), name)
			key = bucket.new_key(key_name)
			key.set_contents_from_filename(file_name)
			key.set_acl('public-read')