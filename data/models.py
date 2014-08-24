from __future__ import division
from django.contrib.auth.models import User
from django.db import models
from django.db import connection
from datetime import datetime, timedelta
from django.db.models import Sum, Avg
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from Crypto.Cipher import Blowfish
import binascii
import shutil
import re

# -----------------------------------------------------------------------------------------------
# FACTORY/
# -----------------------------------------------------------------------------------------------
class Factory(models.Model):

	# READONLY.-
	READONLY=[]

	# PROPERTIES.-
	user	= models.ForeignKey(User,null=False)
	name 	= models.CharField(max_length=20,unique=False,null=False)
        date 	= models.DateTimeField(auto_now=False,auto_now_add=False,null=False,unique=False)

	# META.-
	class Meta:
        	app_label = 'data'
        	abstract = True
		ordering = ['name',]

	# TO STRING.-
	def __str__(self):
       		return self.name

	# CHECK IF THERE IS ANOTHER ELEMENT WITH THE SAME NAME OF ID.-
	@staticmethod
	def existsID(cls,id):
		try: 
			return cls.objects.get(id=id).id>0
		except:	
			return False
	@staticmethod
	def existsName(cls,name):
		try: 
			return cls.objects.get(name=name).id>0
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

	# OVERRIDE.-
	@staticmethod
	def existsID(id): return Factory.existsID(Folder,id)
	@staticmethod
	def existsName(id): return Factory.existsName(Folder,id)

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
		return File.objects.filter(father=self)

	# RETURN PATH TO THIS FOLDER.-
	def short_path(self):
		if self.father and self.father.id:
			return self.father.short_path() + unicode(self.id) + "/"
		else:
			self.id + "/"

	# RETURN FULL PATH TO THIS FOLDER.-
	def full_path(self):
		if self.father and self.father.id:
			return self.father.full_path() + unicode(self.id) + "/"
		else:
			return settings.PROTECTED_MEDIA_ROOT + unicode(self.id) + "/"

	# GET PATH AS AN ARRAY OF OBJETS.-
	def array_path(self):
		ob = self
		ar = []
		while ob.father and ob.father.id:
			ar.append(ob.father)	
			ob = ob.father
		return ar

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

# -----------------------------------------------------------------------------------------------
# UPLOAD TO 
# -----------------------------------------------------------------------------------------------
def get_upload_path(instance, filename):
	return instance.short_path()

# -----------------------------------------------------------------------------------------------
# FACTORY/ FILE/
# -----------------------------------------------------------------------------------------------
class File(Factory):

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
	cmedia_storage = FileSystemStorage(location=settings.PROTECTED_MEDIA_ROOT)

	# META.-
        class Meta(Factory.Meta):
                db_table = "File"

	# PROPERTIES.-
	file = models.FileField(upload_to=get_upload_path, null=False, storage=cmedia_storage)	
	folder = models.ForeignKey("Folder",null=False)
        type = models.CharField(max_length=3,null=False,choices=CHOICES)

	# GET FILE EXTENSION.-
	def extension(self):
        	name, extension = os.path.splitext(self.file.name)
        	return extension

	# GET FULL PATH TO FILE INCLUDING MEDIA ROOT.-
	# EXAMPLE: /var/media/dir1/dir2/file.txt
	def full_path(self):
		return self.father.full_path() + self.filename()

	# GET SHORT PATH THAT DOES NOT INCLUDE MEDIA ROOT.-
	# EXAMPLE: dir1/dir2/file.txt
	def short_path(self):
		return self.father.short_path() + self.filename()

	# GET FILENAME.-
	# EXAMPLE: file.txt
	def filename(self):
		return unicode(self.id) + "." + self.extension()

	# DELETE.-
	def delete(self):
		# REMOVE FILE FROM OS.-
		os.remove(self.full_path())	
		Factory.delete(self)

	# SAVE.-
	def save(self):

		#CHECK FILE TYPE.-
		if self.extention in ['midi','mp3']:
			self.type = 'AUD'
		elif self.extention in ['jpg','png']:
			self.type = 'IMG'
		elif self.extention in ['mp4','mpeg','3gp']:
			self.type = 'VID'
		elif self.extention in ['doc']:
			self.type = 'PDF'
		elif self.extention in ['txt']:
			self.type = 'TXT'
		elif self.extention in ['rar','zip','tar','ear']:
			self.type = 'TAR'
		else:
			self.type = 'OTH'
		
		# SAVE
		Factory.save(self)

