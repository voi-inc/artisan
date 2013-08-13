# stdlib
import os

# 3rd party
import pandoc


# Setup pyandoc
pandoc.core.PANDOC_PATH = '/usr/bin/pandoc'

# Create temporary README.txt
doc = pandoc.Document()
doc.markdown = open('README.md').read()
f = open('README.txt','w+')
f.write(doc.rst)
f.close()

# Register using setup.py
print(os.getcwd())
os.system("sudo python setup.py register")

# Rempve temporary README.txt
os.remove('README.txt')