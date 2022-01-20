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
    ndate = x['date'].split('-')
    d = f'{ndate[2]}-{ndate[1]}-{ndate[0]}'
    region=Region.objects.get(name=x['region'])
    Holidays.objects.create(region=region, date=d, name=x['name'])

def createuser(x):
    try:
        user=User.objects.create_user(username=x['employee_number'],password=x['password'], first_name=x['employee_name'])
    except django.db.utils.IntegrityError:
        print('User already exist.')
        user=User.objects.get(username=x['employee_number'])
    
    print(x['region'])
    region=Region.objects.get(name=x['region'])
    print(region)
    Profile.objects.create(user=user,employee_name=x['employee_name'],role=x['role'],
    rollover=x['rollover'],region=region,lm_start_date=x['lm_start_date'],
    approver=x['approver'],approver_id=user,Gender=x['Gender'],token=x['token'])
   

def updaterec(x):
    t=Profile.objects.get(user=x['employee_number'])
    t.approver_id=User.objects.get(username=x['approver_id'])
    t.save()


Holidays.objects.all().delete()
Region.objects.all().delete()
Region.objects.create(name='General Holidays')

dff=pd.read_csv('holidays.csv')


df=pd.read_excel('Records.xlsx', dtype={'employee_number': str,
                                        'approver_id': str })
rlist = df.region.unique()
for r in rlist:
    Region.objects.create(name=r)  

dff.apply(holidayscreate, axis=1)

print("holidays created")
print("regions created")

df['token'] = df.apply(lambda x: uuid.uuid4(), axis=1)
print(df.shape)
df.to_csv('Profile_details.csv')
df['password']=df['password'].astype(str)
df.apply(createuser,axis=1)
df.apply(updaterec,axis=1)
