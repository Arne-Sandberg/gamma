from __future__ import division
from django.db import models
from django.db import connection
from datetime import datetime, timedelta
from django.db.models import Sum, Avg
from django.conf import settings
from django.contrib.auth.models import User
from Crypto.Cipher import Blowfish
import binascii
import re

# -----------------------------------------------------------------------------------------------
# KAIN ROOT 
# -----------------------------------------------------------------------------------------------
class KainRoot(models.Model):
	
        # -----------------------------------------------------------------------------------------------
        # READONLY.-
        # -----------------------------------------------------------------------------------------------
        READONLY = ['']

	# -----------------------------------------------------------------------------------------------
	# Properties
	# -----------------------------------------------------------------------------------------------
	name	= models.CharField(max_length=40,unique=True,null=False) 	

	# -----------------------------------------------------------------------------------------------
	# META
	# -----------------------------------------------------------------------------------------------
	class Meta: 
		app_label = 'kain'
		abstract = True

	# -----------------------------------------------------------------------------------------------
	# To String.-
	# -----------------------------------------------------------------------------------------------
	def __str__(self): 	
		return self.name

# -----------------------------------------------------------------------------------------------
# FOLDER 
# -----------------------------------------------------------------------------------------------
class KainFolder(KainRoot):

        # -----------------------------------------------------------------------------------------------
        # READONLY.-
        # -----------------------------------------------------------------------------------------------
        READONLY = ['']

	# -----------------------------------------------------------------------------------------------
	# META 
	# -----------------------------------------------------------------------------------------------
	class Meta(KainRoot.Meta):
		db_table = "Folder"

	# -----------------------------------------------------------------------------------------------
	# Exists
	# -----------------------------------------------------------------------------------------------
	@staticmethod
	def exists(s):
		try:
			b = KainFolder.objects.get(id=s)
		except:
			try: 
				b = KainFolder.objects.get(name=s)
			except:
				b = KainFolder()
		if b.id:
			return True
		else:
			return False

	# -----------------------------------------------------------------------------------------------
	# Children
	# -----------------------------------------------------------------------------------------------
	def children(self):
		return Bookmark.objects.filter(folder=self)

# -----------------------------------------------------------------------------------------------
# BOOKMARK
# -----------------------------------------------------------------------------------------------
class Bookmark(KainRoot):

	# -----------------------------------------------------------------------------------------------
	# META 
	# -----------------------------------------------------------------------------------------------
	class Meta(KainRoot.Meta):
		db_table = "Bookmark"
		
	# -----------------------------------------------------------------------------------------------
	# Properties
	# -----------------------------------------------------------------------------------------------
	url	= models.URLField(max_length=255,unique=False,null=True) 	
	folder	= models.ForeignKey("KainFolder",null=True,default="")
	user	= models.CharField(max_length=40,unique=False,null=True) 	
	pasw	= models.CharField(max_length=250,unique=False,null=True) 	

	# -----------------------------------------------------------------------------------------------
	# Exists
	# -----------------------------------------------------------------------------------------------
	@staticmethod
	def exists(s):
		try:
			b = Bookmark.objects.get(id=s)
		except:
			try: 
				b = Bookmark.objects.get(name=s)
			except:
				b = Bookmark()
		if b.id:
			return True
		else:
			return False

        # -----------------------------------------------------------------------------------------------
	# ENCRYPTION
        # -----------------------------------------------------------------------------------------------

	# Set
	def _get_ssn(self):
        	enc_obj = Blowfish.new( settings.SECRET_KEY )
		try: 
        		return u"%s" % enc_obj.decrypt( binascii.a2b_hex(self.pasw) ).rstrip()
		except:
			return ""

	# Get
    	def _set_ssn(self, ssn_value):
        	enc_obj = Blowfish.new( settings.SECRET_KEY )
        	repeat = 8 - (len( ssn_value ) % 8)
        	ssn_value = unicode( ssn_value + " " * repeat )
        	self.pasw = binascii.b2a_hex(enc_obj.encrypt( ssn_value ))

	# Property
    	password = property(_get_ssn, _set_ssn)
