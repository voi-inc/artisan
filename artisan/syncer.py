# stdlib
import os
import shutil

# 3rd party
import boto


class LocalSyncer(object):
    """
    Mirror img directory locally
    """
    def get_base_url(self):
        """
        Return the base url for path rewrites. In this case, because we are
        mirroring locally, it should be an empty string.
        """
        return ''

    def mirror(self, src_dir, dest_dir, img_dir):
        """
        Copy, if any, src images to dest directory
        """
        img_src_dir = os.path.join(img_dir, 'images')
        img_dest_dir = img_src_dir.replace(src_dir, dest_dir)
        # If there is a src img directory
        if os.path.isdir(img_src_dir):
            # Remove existing images
            if os.path.exists(img_dest_dir):
                shutil.rmtree(img_dest_dir)
            # Copy over all images
            shutil.copytree(img_src_dir, img_dest_dir)


class AwsSyncer(object):
    """
    Mirror img directory to amazon s3 using boto
    """
    def __init__(self, storage):
        self.storage = storage

    def get_base_url(self):
        """
        Return the base url for path rewrites.
        """
        return 'https://s3.amazonaws.com/{}/'.format(self.storage['bucket'])

    def mirror(self, src_dir, dest_dir, img_dir):
        """
        Sync image assets from specified directory to Amazon S3.
        """
        conn = boto.connect_s3(
            aws_access_key_id=self.storage['aws_access_key_id'],
            aws_secret_access_key=self.storage['aws_secret_access_key']
        )
        # Create bucket if it does not exist
        bucket = conn.lookup(self.storage['bucket'])
        if bucket is None:
            bucket = conn.create_bucket(self.storage['bucket'])
        # Add all images and make public
        img_src_dir = os.path.join(img_dir, 'images')
        for name in os.listdir(img_src_dir):
            file_name = os.path.join(img_src_dir, name)
            key_name = os.path.join(img_src_dir.replace(src_dir, ''), name)
            key = bucket.new_key(key_name)
            key.set_contents_from_filename(file_name)
            key.set_acl('public-read')
