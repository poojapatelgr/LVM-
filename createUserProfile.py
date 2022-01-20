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

df=pd.read_excel('/home/sikshana/Leaveapp/NewUsers.xlsx', dtype={'employee_number': str,
                                                                          'approver_id': str })

df['token'] = df.apply(lambda x: uuid.uuid4(), axis=1)
print(df.shape)
df.to_csv('NewUsersToken.csv')
df['password']=df['password'].astype(str)
df.apply(createuser,axis=1)
df.apply(updaterec,axis=1)
