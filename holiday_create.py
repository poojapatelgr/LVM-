#!/usr/bin/env python3
import pandas as pd
import numpy as np
import random
import datetime
import uuid
from django.contrib.auth.models import User
import django
from leaveman.models import Region
from leaveman.models import Holidays
from leaveman.models import Profile
from leaveman.models import records

print('HIII')

def holidayscreate(x):
    region=Region.objects.get(name=x['region'])
    print(region, x)
    Holidays.objects.create(region=region, date=x['date'], name=x['name'])


dff=pd.read_csv('holidays.csv', parse_dates=["date"])
dff.apply(holidayscreate, axis=1)
