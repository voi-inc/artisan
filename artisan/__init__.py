# stdlib
import os
import json
import argparse

# artisan
from utils import merge
from artisan import Artisan


#
# Load Json and return data
#
def getConfig(path):

	# Config defaults
	default = {
		"port": 8080,
		"src": os.path.join(os.getcwd(), 'src'),
		"dest": os.path.join(os.getcwd(), 'build')
	}

	# Open, parse data, and close
	file = open(path)
	data = json.load(file)
	file.close()

	# Merge and return
	return merge(default, data)


#
# Run when called from console
#
def console():

	# Command line parser
	parser = argparse.ArgumentParser(description='Start web server using passed directory and port')
	parser.add_argument('method', help='directory to serve from', type=str, choices=['craft', 'ship'])
	args = parser.parse_args()

	# Get config
	configPath = os.path.join(os.getcwd(), 'artisan.json')
	config = getConfig(configPath)

	# Run program
	artisan = Artisan(config['src'], config['dest'], config['port'], config['aws'])
	if args.method == 'craft':
		artisan.craft()
	else:
		artisan.ship()


# Do not run if imported
if __name__ == '__main__':
	console()