from django.forms import ModelForm
from django.db import models

# Retrieves an object 
# It's similar to get_or_404 but without exceptions
# ----------------------------------------------------
def retrieve(cls,**kwargs):
        try:    return cls.objects.get(**kwargs)
        except: return cls(**kwargs)

# For a given model, retrieve required and 
# non-required fields.-
# ----------------------------------------------------
def getfields(cls):
	req 	= []
       	non 	= []
	ro	= cls.READONLY
       	for a in cls._meta.fields:
       		if a.name == "id":      pass
		elif a.name in ro:	pass
               	elif a.null:            non.append(a.name)
               	else:                   req.append(a.name)
        return req, non
	
# For a given form, retrieve a form class.-
# ----------------------------------------------------
def getform(cls,fields=(),readonly=()):
	class MyForm(ModelForm):
		class Meta: 
			model  = cls
	if fields:
		MyForm.Meta.fields = fields
	if readonly:
		MyForm.Meta.readonly_fields = readonly
	return MyForm
