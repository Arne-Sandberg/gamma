from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from optparse import make_option
from django.conf import settings
from datetime import datetime
from folder.models import *
import sys
import os

class Command(BaseCommand):
	
	# Display help.-
    	help = 'upload -n <name> -f <file> -F <folderID>'

	# Arguments.-
	option_list = BaseCommand.option_list + (
        		make_option('-n', 	dest='name',	help='File name',		),
        		make_option('-f', 	dest='file',	help='Upload file',		),
        		make_option('-F', 	dest='folder',	help='Destintion folder',	),
    	)

	# Handle requests.-
    	def handle(self, *args, **options):

		# Dispatch.-
		path = options.get('file')
		dest = int(options.get('folder',0))
		name = options.get('name',0)

		# Create folder.-
		folder = Folder.objects.get(id=dest)	
		dest_path = folder.full_path() 
        	self.stdout.write("Writing to %s" % dest_path )

		# Create file.-
		localfile = open(path)
		djangofile = File(localfile)
        	self.stdout.write("Working with %s" % path )

		# Get user.-
		user = User.objects.get(username='martin')
        	self.stdout.write("Working as %s" % user.username )

		# Crete django file.-
		file = GFile()
		file.date = datetime.now()
		file.folder = folder
		file.file = djangofile
		file.setName(name)
		file.user = user

		# End.-
		file.save()
		localfile.close()
        	self.stdout.write("Done!")
