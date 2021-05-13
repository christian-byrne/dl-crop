#! /usr/bin/python

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/bymyself/_BYMYself/bmp')
from DL_and_Trim import app as application
application.secret_key = 'drpeper5'




