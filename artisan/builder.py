# stdlib
import os
import shutil

# 3rd party
from jinja2 import Environment, FileSystemLoader
from premailer import transform

# artisan
import utils

class Builder(object):
    """
    Contains assets that builds and syncs data. This is the engine of the
    artisan package.
    """
    def __init__(self, src_dir, dest_dir, syncer):
        # Cache dirs
        self.src_dir = src_dir
        self.dest_dir = dest_dir
        # Cache syncer
        self.syncer = syncer

    def build(self):
        """
        Build all masters and all messages.
        """
        self.copy_masters_imgs()
        self.build_messages()

    def build_single(self, path):
        """
        Build a single template by building a single message and copying
        over all masters imgs
        """
        self.build_message(path)

    def build_messages(self):
        """
        Loop over all messages and build each html file. Also, sync 
        images in eacher message directory
        """
        message_tmpls_dir = os.path.join(self.src_dir, 'messages')
        for dir_name, dir_path in utils.each_subdir(message_tmpls_dir):
            self.build_message(dir_path)

    def build_message(self, path):
        """
        Write message templates and copy dir imgs
        """
        for file_name, file_path in utils.each_tmpl(path):
            self.write_template(file_path)
        self.mirror_imgs(path)

    def copy_masters_imgs(self):
        """
        Loop over all masters and copy images.
        """
        master_tmpls_dir = os.path.join(self.src_dir, 'masters')
        for dir_name, dir_path in utils.each_subdir(master_tmpls_dir):
            self.mirror_imgs(dir_path)

    def mirror_imgs(self, img_path):
        """
        Mirror images in src_dir to dest_dir
        """
        self.syncer.mirror(self.src_dir, self.dest_dir, img_path)

    def write_template(self, path):
        """
        Write template out to specified output directory.
        """
        # Cache paths
        rel_src_file = path.replace(self.src_dir, '')
        abs_dest_file = os.path.join(self.dest_dir, rel_src_file.strip('/'))
        abs_dest_dir = os.path.split(abs_dest_file)[0]
        # Setup jinja root path. Get and render.
        self.jinja = Environment(loader=FileSystemLoader(self.src_dir))
        tmpl = self.jinja.get_template(rel_src_file).render()
        # If html then inline css
        if path.lower().endswith(".html"):
            tmpl = transform(tmpl, base_url=self.syncer.get_base_url())
        # Create dir if it does not exist
        if not os.path.isdir(abs_dest_dir):
            os.makedirs(abs_dest_dir)
        # Save tmpl to file
        with open(abs_dest_file, 'w+') as file:
            file.write(tmpl)

    def remove(self, src_path):
        dest_path = src_path.replace(self.src_dir, self.dest_dir)
        if os.path.exists(dest_path):
            if os.path.isfile(dest_path):
                os.remove(dest_path)
            else:
                shutil.rmtree(dest_path)
