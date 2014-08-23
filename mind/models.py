from __future__ import division
from django.db import models
from django.db import connection
from datetime import datetime, timedelta
from django.db.models import Sum, Avg
from django.conf import settings
from django.contrib.auth.models import User
from Crypto.Cipher import Blowfish
from libs.shared import * 
import binascii
import re

# -----------------------------------------------------------------------------------------------
# CHAPTER IMAGE
# -----------------------------------------------------------------------------------------------
class ChapterImage(models.Model):
	
	# Properties
	chapter = models.OneToOneField('Chapter',related_name='image')
	img 	= models.FileField(upload_to='mind/', null=True)

	# Set new file 
        def set_img(self,image):
		if not FileMedia.validate_img_extension(file=image):
			raise Exception('Invalid image!')
		if not FileMedia.validate_size(file=image,size=20242880): 
			raise Exception('File too large!')
		FileMedia.set_file( self, 'img', image )

	# META.-
	class Meta: 
		app_label = 'mind'
		db_table = "mChapterImage"

        # READONLY
        READONLY = ['']

# -----------------------------------------------------------------------------------------------
# CHAPTER
# -----------------------------------------------------------------------------------------------
class Chapter(models.Model):

        # READONLY
        READONLY = ['']

	# Properties
	title		= models.CharField(max_length=20,unique=True,null=False) 	
	subtitle	= models.CharField(max_length=40,unique=False,null=False) 	

	# To String.-
	def __str__(self): 	
		return '%s' % (self.title)

	# META.-
	class Meta: 
		app_label = 'mind'
		ordering = ['id']
		db_table = "mChapter"

# -----------------------------------------------------------------------------------------------
# SINGLE 
# -----------------------------------------------------------------------------------------------
class Page(models.Model):

        # READONLY
        READONLY = ['']

	# Properties
	title 	= models.CharField(max_length=40,unique=False,null=False) 	
	text	= models.CharField(max_length=8000,unique=False,null=False) 	
        date 	= models.DateField(auto_now=False,auto_now_add=False,null=False,unique=False)
	chapter = models.ForeignKey('Chapter')

	# To String.-
	def __str__(self): 	
		return '%s' % (self.title)

	# META.-
	class Meta: 
		app_label = 'mind'
		ordering = ['id']
		db_table = "mText"
