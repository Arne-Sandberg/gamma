from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db import models
import os
import re

""" Checks File System size """
""" 
def df(mountpoint):
        s = os.statvfs(mountpoint)
        return (s.f_bavail * s.f_frsize) / 1024
"""

""" Handles protected storage """
cmedia_storage = FileSystemStorage(location=settings.PROTECTED_MEDIA_ROOT, base_url='/var/phi/protected/')

class FileMedia(models.Model):

        """ Check file extension """
	@staticmethod
        def validate_img_extension(file):
                extension = file.name.split('.')[-1]
                return re.match( r'jpg|png|jpeg', extension )

        """ Check file size """
	@staticmethod
        def validate_size(file,size=10242880):
                return file.size < size

	""" Deletes old file """
	@staticmethod
	def set_file(obj,field_name,new_file):
		file = getattr(obj, field_name)
		if file and file.name:
			os.remove(file.path)
                setattr( obj, field_name, new_file)

