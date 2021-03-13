"""
Provide access to gentb database without the website.
"""

import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tb_website.settings.gentb")

import django
from django.core.management import execute_from_command_line

django.setup()

from django.conf import settings
from django.db import connections
from django.db.utils import OperationalError

from apps.maps.models import *
from apps.mutations.models import *
from apps.pipeline.models import *
from apps.predict.models import *
from apps.uploads.models import *

if settings.DB_IS_FILE and not os.path.isfile(settings.DB_NAME):
    print("""
  You have a new database {} that must be created,
    use gentb.migrate() to create the schema
    and gentb.loaddata(filename) to load a json file
    the gentb.dumpdata(filename) is also available to output data.

  """.format(settings.DB_NAME))

db_conn = connections['default']
try:
    db_cursor = db_conn.cursor()
except OperationalError as err:
    sys.stderr.write("\nCan't connect to database: {}\n\n".format(err[1]))


def _cmd(*args):
    """Mask the sys.exit command to stop exiting and return value instead"""
    ret = -1
    def _wrap_exit(code=0):
       ret = code
    _exit, sys.exit = sys.exit, _wrap_exit
    execute_from_command_line([''] + list(args))
    sys.exit = _exit
    return ret


def migrate():
    _cmd('migrate')

def loaddata(filename):
    _cmd('loaddata', filename)

def dumpdata(filename):
    _cmd('dumpdata', '--indent=2', '-o', filename)

