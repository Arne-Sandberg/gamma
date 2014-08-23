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
