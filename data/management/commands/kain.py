from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from kain2.models import *
import sys

class Command(BaseCommand):
	
	# Display help.-
    	help = 'kain -(i|u|p|s) regexp [value]'

	# Arguments.-
	option_list = BaseCommand.option_list + (
        		make_option('-i', 	dest='show',	help='Delete poll',	),
        		make_option('-u', 	dest='user', 	help='Close poll'	),
        		make_option('-p', 	dest='pasw',	help='Close poll'	),
        		make_option('-s', 	dest='save',	help='Close poll'	),
    	)

	# Handle requests.-
    	def handle(self, *args, **options):

		# Dispatch.-
		show = options.get('show')
		user = options.get('user')
		pasw = options.get('pasw')
		save = options.get('save')

		# Regexp lookup.-
		if show:	 	r = show
		elif user: 		r = user 
		elif pasw:		r = pasw
		try: 			
			bk = Bookmark.objects.get(id=r)
		except:			
			try:
				bk = Bookmark.objects.get(name__iregex=r)
			except:
				print "The regexp return more than one valid key!!!!"
				for b in Bookmark.objects.filter(name__iregex=r):
					print b.name
				sys.exit(0)

		# If show and save, store password
		if show and save:
			old = bk.password
			bk.password = save
			bk.save()
        		self.stdout.write("%s Saved!" 		% bk.name)
        		self.stdout.write("%s" 			% bk.name)
        		self.stdout.write("user %s" 		% bk.user)
        		self.stdout.write("old  %s --> out!" 	% old)
        		self.stdout.write("pass %s <-- in! " 	% bk.password)

		# Show all.-
		elif show:
        		self.stdout.write("%s" 		% bk.name)
        		self.stdout.write("user %s" 	% bk.user)
        		self.stdout.write("pass %s" 	% bk.password)

		# Show user.-
		elif user:
        		self.stdout.write(bk.user)

		# Show pasw.-
		elif pasw:
        		self.stdout.write(bk.password)

		# No options.-
		else:
        		self.stdout.write("Nothing to show")
			
