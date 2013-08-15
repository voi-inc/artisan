# stdlib
import os
import time
import shutil
import boto

# 3rd party
from jinja2 import Environment, FileSystemLoader
from premailer import transform


class Builder(object):
    """
    Contains assets that builds and syncs data. This is the engine of the
    artisan package.
    """

    def __init__(self, type, src, dest, aws=None):
        # Defaults / Options
        self.type = type
        self.src = src
        self.dest = dest
        # Make sure we have creds for cloud push
        if type != 'local':
            if not aws:
                raise ValueError('Must provide credentials')
            self.aws = aws
        # Master & Child Templates
        self.master_tmpls = os.path.join(self.src, 'masters')
        self.message_tmpls = os.path.join(self.src, 'messages')
        # Setup jinja root path
        self.jinja = Environment(loader=FileSystemLoader(self.src))

    def build(self):
        """
        Build all masters and all messages.
        """

        self.build_masters()
        self.build_messages()

    def build_masters(self):
        """
        Loop over all masters and sync data.
        """

        for name in os.listdir(self.master_tmpls):
            self.sync(os.path.join(self.master_tmpls, name))

    def build_messages(self):
        """
        Loop over all messages and build each html file. Also, sync 
        images in eacher message directory
        """

        for dir_name in os.listdir(self.message_tmpls):
            message_dir = os.path.join(self.message_tmpls, dir_name)
            # Loop through all files in message dir
            for file_name in os.listdir(message_dir):
                # if html write
                file_path = os.path.join(message_dir, file_name)
                self.write_template(file_path)
            # sync dir images
            self.sync(message_dir)

    def build_message(self, path):
        """
        Build one message.
        """

        self.build_masters()
        self.write_template(path)
        self.sync(path)

    def write_template(self, path):
        """
        Write template out to specified output directory.
        """

        # automatically exit if not file is empty or not a template
        if os.stat(path).st_size == 0 or not self.is_template(path):
            return
        # rel path is used by jinja
        rel_path = path.replace(self.src, '')
        # template
        tmpl = self.jinja.get_template(rel_path)
        # move styles inline
        if (self.type == 'local'):
            if path.endswith(".txt"):
                tmpl = tmpl.render()
            else:
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

    def sync(self, path):
        """
        Determine and call appropriate sync method.
        """

        # src img directory
        img_dir = os.path.join(path, 'images')
        # only relevent if images exist
        if os.path.isdir(img_dir):
            if (self.type == 'local'):
                return self.sync_local(img_dir)
            else:
                self.sync_cloud(img_dir)

    def sync_local(self, dir):
        """
        Determine and call appropriate sync method.
        """

        dest = dir.replace(self.src, self.dest)
        if os.path.exists(dest):
            shutil.rmtree(dest)
        shutil.copytree(dir, dest)

    def sync_cloud(self, dir):
        """
        Sync image assets from specified directory to Amazon S3.
        """

        conn = boto.connect_s3(
            aws_access_key_id=self.aws['aws_access_key_id'],
            aws_secret_access_key=self.aws['aws_secret_access_key']
        )

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

    def is_template(self, path):
        if path.endswith(".html") or path.endswith(".txt"):
            return True
        else:
            return False
