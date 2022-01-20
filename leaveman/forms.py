from django.forms import ModelForm
from leaveman.models import records, Profile, Holidays, LeavesPerYear
from django import forms
from django.utils.translation import gettext_lazy as _
from django.db.models import Count, Q, Sum
from django.core.exceptions import ValidationError
from django.core import validators
from datetime import date, datetime, timedelta
from django.contrib.auth.models import User
import pandas as pd
import numpy as np

def applied_leave(from_date, num_days, user):
    '''

    '''
    l = []
    print(f'applied_leave: {from_date}, {num_days}, {user}')
    #fdate = datetime.strptime(from_date, '%Y-%m-%d')
    user_profile = Profile.objects.get(user=user)

    holidays = Holidays.objects.all().filter(region=user_profile.region)

    holidaystr = [x.date.strftime('%d-%m-%Y') for x in holidays]

    lapplied_date = datetime.combine(from_date, datetime.min.time())
    print(f'applied_leave: {lapplied_date}')

    while True:
        if lapplied_date.isoweekday() == 7 or lapplied_date.strftime('%d-%m-%Y') in holidaystr:
            pass 
        else:
            l.append(lapplied_date.date())

        lapplied_date += timedelta(days=1)
        print(len(l), num_days)
        print(type(num_days))
        if len(l) == num_days:
            print("inloop",l, num_days)
            break

    return l

class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class LeaveForm(ModelForm):

    class Meta:
        model = records
        fields = ['user', 'reason', 'leave_period', 'from_date', 'num_days']
        widgets = {'user': forms.HiddenInput()}
        
    def __init__(self, *args, **kwargs):
        print(f'kwargs: {kwargs}')
        super(LeaveForm, self).__init__(*args, **kwargs)
        print(f'kwargs: {kwargs}')
        self.fields['from_date'] = forms.DateField(widget=DateInput())
        self.fields['num_days'] = forms.IntegerField()
        if 'initial' in kwargs:
            print('RRRRR:',kwargs['initial'])
            remainingpl = kwargs['initial']['rempl']
            remainingsl = kwargs['initial']['remsl']
            ml = kwargs['initial']['ml']
            self.fields['user'] = forms.CharField(
                widget=forms.HiddenInput, required=False, initial=kwargs['initial']['user'])
            self.fields['num_days'] = forms.IntegerField(initial=kwargs['initial']['num_days'])
            choices = self.get_reason_choices(self.fields['reason'].choices,
            kwargs['initial']['gender'], kwargs['initial']['role'], remainingpl, remainingsl, ml)
            self.fields['reason'] = forms.ChoiceField(required=True, choices=choices)
        print(self.fields['reason'].choices)

    def get_reason_choices(self, choices, gender, role, remainingpl, remainingsl, ml):
        nchoices = choices
        if gender == 'M' or role:
            nchoices = [x for x in nchoices if x[0] != 'MATER']
        if gender == 'F' or role:
            nchoices = [x for x in nchoices if x[0] != 'PATER']

        if remainingpl > 0:
            nchoices = [x for x in nchoices if x[0] != 'LOPFD']
            nchoices = [x for x in nchoices if x[0] != 'LOPHD']

        if remainingpl <= 0:
            nchoices = [x for x in nchoices if x[0] != 'PERFD']
            nchoices = [x for x in nchoices if x[0] != 'PERHD']

        if remainingsl <= 0:
            nchoices = [x for x in nchoices if x[0] != 'SICFD']
            nchoices = [x for x in nchoices if x[0] != 'SICHD']

        if ml:
            nchoices = [x for x in nchoices if x[0] != 'MARRY']

        return nchoices
        
    def clean_from_date(self):
        print('SELFCDATT:',self.cleaned_data)
        user = self.cleaned_data['user']
        from_date = self.cleaned_data['from_date']
        reason = self.cleaned_data['reason']
        leave_period = self.cleaned_data['leave_period']
        if 'num_days' in self.cleaned_data:
            num_days = self.cleaned_data['num_days']
        else:
            num_days = 1


        matdays = LeavesPerYear.objects.all().first().mt
        mtrec = records.objects.filter(user=user,reason='MATER')
        if mtrec:
            mrec = mtrec.first()
            frdt = mrec.from_date
            todt = frdt + timedelta(days=matdays-1)
            if frdt <= from_date <= todt:
                raise ValidationError(f'You have already applied for maternity leave from {frdt} till {todt}.')
    
        print(from_date, date.today())
        today = datetime.now()
        tillday = today + timedelta(days=30)
        if (from_date + timedelta(7)) < today.date() or from_date > tillday.date():
            raise ValidationError("From Date has to in the range from today to within 30 days from today.")

        userobj = User.objects.get(username=user)
        user_profile = Profile.objects.get(user=userobj)
        dates = records.objects.filter(user=userobj)
        dates = [x.from_date for x in dates]
        print(f'dates taken: {dates}')
        holidays = Holidays.objects.all().filter(region=user_profile.region)
        
        dates_req = applied_leave(
            from_date,
            int(num_days),
            userobj
        )
        print(f'dates_req: {dates_req}')
        dates_reqs = set(dates_req)
        dates_taken  = set(dates)
        inter = list(dates_taken.intersection(dates_req))
        print('inter:', inter)
        print('dates_taken:',dates_taken)
        #if inter and reason != 'HD'

        if inter:
            leaveperiod_choices={
            'FIRHALF':'First Half',
            'SECHALF':'Second Half',
            }
            tdate = inter[0]
            rec=records.objects.filter(user=userobj,from_date = tdate)
            print('RECCCCCCC:',rec.first().leave_period,reason,leave_period)
            if 'HD' in rec.first().reason and 'HD' in reason and len(rec)==1 and leaveperiod_choices[leave_period] != rec.first().leave_period:
                return from_date
            dates = [x.strftime("%b %d %Y") for x in inter]
            dates = ", ".join(dates)
            raise ValidationError(f'You have already applied for leave for the days: {dates}.')
        return from_date

    def clean(self):
        super().clean()
        print(f'clean: cleaned_data: {self.cleaned_data}')
        reasonc = self.cleaned_data['reason']
        if reasonc == 'MATER' or reasonc == 'PATER':
            userc = self.cleaned_data['user']
            today = datetime.now()
            tillday = today - timedelta(days=365)
            mpdates = records.objects.filter(user=userc, from_date__gte = tillday,reason=reasonc)
            if mpdates:
                r = {'MATER': 'Maternity', 'PATER': 'Paternity'}
                raise ValidationError(f'You have already availed {r[reasonc]} leave in the last 365 days.')
        
        if reasonc == 'MARRY':
            userc = self.cleaned_data['user']
            mardates = records.objects.filter(user=userc,reason=reasonc)
            if mardates:
                raise ValidationError(f'You have already availed Marriage leave.')


class ExportCSVForm(forms.Form):
    from_date = forms.DateField(widget = DateInput())
    to_date = forms.DateField(widget = DateInput())
    ROLE_CHOICES = (
        (False,"Employees"),
        (True,"Consultants"),
        )
    role = forms.ChoiceField(choices = ROLE_CHOICES)

    def clean(self):
        super().clean()
        if self.cleaned_data['from_date'] > self.cleaned_data['to_date']:
            print('Validation not working')
            raise ValidationError(f'From date is greater than To date')


def getrecyears():
    objects = [x.year for x in records.objects.all()]
    years = np.unique(np.array(objects))
    return ((x,x) for x in years)


class EmpHistoryForm(forms.Form):
    employee_number = forms.CharField(max_length=20)
    year =  forms.ChoiceField(choices = getrecyears())

    def clean(self):
        super().clean()
        l=User.objects.filter(username=self.cleaned_data['employee_number'])
        print(l.exists())
        if not l.exists():
            raise ValidationError(f'Employee Number does not exist.')
            

class TokenForm(forms.Form):
    token=forms.CharField(label='Token',max_length=500)
