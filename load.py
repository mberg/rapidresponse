# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.join(os.getcwd(),'lib'))

# override the standard method for running this
# so that we can include settings.py and our own
# settings

from rapidsms.config import Config
from rapidsms.manager import Manager
from django.core.management import execute_manager, setup_environ

# we know it will be rapidsms.ini in this projects
os.environ["RAPIDSMS_INI"] = "rapidsms.ini" 
os.environ["DJANGO_SETTINGS_MODULE"] = "settings.py"

conf = Config(os.environ["RAPIDSMS_INI"])
import settings
setup_environ(settings)

from datetime import datetime, timedelta
from apps.sms.models.base import ReportMalnutrition, Case, Zone, Facility
from apps.sms.views.reporting import MalawiReport, MalawiNew
from apps.sms.views.joining import MalawiJoin

from random import choice

class FakeMessage:
    def __init__(self, number):
        self.peer = self.sender = number
        
    def respond(self, *args, **kw):
        print args[0]

now = datetime.now()

fm = FakeMessage("1234567")
MalawiJoin(fm, "15 Andy McKay")()
MalawiNew(fm, "50 15 M 19102008 123124124")()
muac = 130
height = 100
for x in range(0, 100):
    muac -= 1
    height -= 0.5
    MalawiReport(fm, "50 25.2 %s %s N Y" % (height, muac))()
    res = ReportMalnutrition.objects.filter(case=1).latest("entered_at")
    res.entered_at = now - timedelta(days=x)
    res.save()

fm = FakeMessage("999999")
MalawiJoin(fm, "162 Coulibaly Mariam")()
MalawiNew(fm, "70 1201 M 19102008 123124124")()
muac = 150
height = 10
for x in range(0, 100):
    muac -= 1
    height += 0.5
    MalawiReport(fm, "70 25.2 95.5 %s N Y" % muac)()
    res = ReportMalnutrition.objects.filter(case=2).latest("entered_at")
    res.entered_at = now - timedelta(days=x * 2)
    res.save()
