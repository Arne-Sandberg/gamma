from __future__ import division
from django.contrib.auth.models import User
from django.db import models
from django.db import connection
from datetime import datetime, timedelta
from django.db.models import Sum, Avg
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from Crypto.Cipher import Blowfish
import random
import os
import binascii
import shutil
import re
import time

# -----------------------------------------------------------------------------------------------
# FACTORY/
# -----------------------------------------------------------------------------------------------
class Factory(models.Model):

	# READONLY.-
	READONLY=[]

	# PROPERTIES.-
	user	= models.ForeignKey(User,null=False)
	name 	= models.CharField(max_length=75,unique=False,null=False)
        date 	= models.DateTimeField(auto_now=False,auto_now_add=False,null=False,unique=False)

	# META.-
	class Meta:
        	app_label = 'folder'
        	abstract = True
		ordering = ['name',]

	# TO STRING.-
	def __str__(self):
       		return self.name

	# CHECK IF THERE IS ANOTHER ELEMENT BY ID.-
	@staticmethod
	def existsID(cls,id):
		try: 
			return cls.objects.get(id=id).id>0
		except:	
			return False

# -----------------------------------------------------------------------------------------------
# FACTORY/ FOLDER/
# -----------------------------------------------------------------------------------------------
class Folder(Factory):

	# PROPERTIES
	# read: True if is public. False if only admins can see the file.-
	# write: True if anybody can upload files. False if only admins may upload files.-
	read	= models.BooleanField(default=False)	
	write 	= models.BooleanField(default=False)
	father 	= models.ForeignKey("Folder",null=True)

	# READONLY.-
	READONLY=[]

	# META.-
        class Meta(Factory.Meta):
                db_table = "Folder"
		ordering = ['name',]

	# OVERRIDE.-
	@staticmethod
	def existsID(id): return Factory.existsID(Folder,id)

	# ON DELETE: CASCADE AND DELETE FOLDER.-
	def delete(self):
		# REMOVE FOLDER AND ALL IT's CONTENTS.-
		try:
			shutil.rmtree(self.full_path())
		except Exception as e:
			print e
		Factory.delete(self)

	# RETURN ALL ELEMENTS CHECKING PERMISSIONS.-
	def children(self,user):	
		if user.is_superuser:
			return Folder.objects.filter(father=self)
		else:
			return Folder.objects.filter(father=self,read=True)

	# RETURN ALL ELEMENTS.-
	def allChildren(self):	
		return Folder.objects.filter(father=self)

	# RETURN A REFERENCE TO THE ROOT ELEMENT.-
	@staticmethod
	def root(user):
		if user.is_superuser:
			return Folder.objects.filter(father=None)
		else:
			return Folder.objects.filter(father=None,read=True)

	# RETURN A LIST OF CHILDREN FILES.-
	def files(self):		
		return GFile.objects.filter(folder=self)

	# RETURN PATH TO THIS FOLDER.-
	def short_path(self):
		if self.father and self.father.id:
			return self.father.short_path() + unicode(self.id) + "/"
		else:
			return unicode(self.id) + "/"

	# RETURN FULL PATH TO THIS FOLDER.-
	def full_path(self):
		if self.father and self.father.id:
			return self.father.full_path() + unicode(self.id) + "/"
		else:
			return settings.MEDIA_ROOT + unicode(self.id) + "/"

	# GET PATH AS AN ARRAY OF OBJETS.-
	def array_path(self):
		ob = self
		ar = []
		while ob.father and ob.father.id:
			ar.append(ob.father)	
			ob = ob.father
		return reversed(ar)

	# SET READ RECURSIVELY
	def setRead(self,boolean):
		for c in self.allChildren():
			c.setRead(boolean)
		self.read = boolean
		self.save()

	# SET WRITE RECURSIVELY
	def setWrite(self,boolean):
		for c in self.allChildren():
			c.setWrite(boolean)
		self.write= boolean
		self.save()

	# GET PLAYLIST 
	def playlist(self,user):
		qs = self.files()
		for c in self.children(user):
			qs = qs | c.playlist(user)
		return qs

# -----------------------------------------------------------------------------------------------
# UPLOAD TO 
# MEDIA_ROOT + folder.path + timestamp + extension
# -----------------------------------------------------------------------------------------------
def get_upload_path(instance, filename):
        name, extension = os.path.splitext(filename)
	path = instance.folder.short_path()
	ts   = time.time()
	rand = random.randint(10000000000,999999999999999)
	return "%s%d_%d%s" % (path,ts,rand,extension)

# -----------------------------------------------------------------------------------------------
# FACTORY/ FILE/
# -----------------------------------------------------------------------------------------------
class GFile(Factory):

	# READONLY.-
	READONLY=[]

	# FILE TYPES.-
	CHOICES = (
    			('IMG', 'Imagen'),
    			('AUD', 'Audio'),
    			('VID', 'Video'),
    			('PDF', 'PDF'),
    			('TXT', 'Texto'),
    			('TAR', 'Archivo comprimido'),
    			('OTH', 'Otro'),
	)
	
	# PRIVATE UPLOADS.-
	cmedia_storage = FileSystemStorage(location=settings.MEDIA_ROOT)

	# META.-
        class Meta(Factory.Meta):
                db_table = "File"

	# PROPERTIES.-
	file = models.FileField(upload_to=get_upload_path, null=True, storage=cmedia_storage)	
	folder = models.ForeignKey("Folder",null=False)
        type = models.CharField(max_length=3,null=False,choices=CHOICES)
        mime = models.CharField(max_length=20,null=False,choices=CHOICES)

	# FILE NAME
	# EXAMPLE: txt
	def extension(self):
        	name, extension = os.path.splitext(self.file.name)
        	return extension
	# EXAMPLE: file
	def filename(self):
        	name, extension = os.path.splitext(self.file.name)
        	return name

	# CHECK FILE SIZE
	def checkSize(self):
		if self.file.size < settings.TASK_UPLOAD_FILE_MAX_SIZE:
			return True
		else:
			return False

	# DELETE.-
	def delete(self):
		# REMOVE FILE FROM OS.-
		os.remove(settings.MEDIA_ROOT+self.file.name)
		Factory.delete(self)

	# SET NAME.-
	def setName(self,new_name=None):
		if new_name:
			n = new_name
		else:
			n = self.file.name
        	name, extension = os.path.splitext(n)
		if not extension: 
			extension = self.extension()
		ext_count = len(extension)
		self.name = name[:75-ext_count] + self.extension()

	# SAVE.-
	def save(self):

		#CHECK FILE TYPE.-
		if self.extension() in ['.mid','.mp3']:
			self.type = 'AUD'
		elif self.extension() in ['.jpg','.png','.jpeg','.gif']:
			self.type = 'IMG'
		elif self.extension() in ['.mp4','.mpeg','.3gp','.ogv','.ogg','flv',]:
			self.type = 'VID'
		elif self.extension() in ['.pdf']:
			self.type = 'PDF'
		elif self.extension() in ['.txt']:
			self.type = 'TXT'
		elif self.extension() in ['.rar','.zip','.tar','.ear']:
			self.type = 'TAR'
		else:
			self.type = 'OTH'
			
		# SAVE
		Factory.save(self)

	# OVERRIDE.-
	@staticmethod
	def existsID(id): return Factory.existsID(GFile,id)

	# ARRAY PATH
	def array_path(self):
		d = [[self.folder.id,self.folder.name]]
		for c in self.folder.array_path():
			d.append([c.id,c.name])
		return d

	# SERIALIZE OBJECT.-
	def serialize(self):
		d = {
                	"name":         self.name,
                	"id":           self.id,
                	"folder_id":    self.folder.id,
                	"folder_name":  self.folder.name,
                	"fname":        self.file.name,
                	"ftype":        self.type,
               		"path":         [],
        	}
		for p in self.folder.array_path():
			d['path'].append([ p.id, p.name ])
		return d 
	

