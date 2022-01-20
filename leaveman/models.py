from django.db import models
from django.contrib.auth.models import User
from datetime import date
from uuid import uuid4
   

class Region(models.Model):

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Holidays(models.Model):

    class Meta:
        verbose_name = 'Holidays for Different Regions'
        verbose_name_plural = 'Holidays for Different Regions'
    
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    date = models.DateField()
    name = models.CharField(max_length=200)

    
    def __str__(self):
        return self.name

class LeavesPerYear(models.Model):
    
    '''
    ro: max rollover
    pl: Personal Leave
    sl: Sick Leave
    ml: Maternity Leave
    ma: Marriage
    pt: Paternity
    '''

    class Meta:
        verbose_name = 'Official Leave Policy Numbers'
        verbose_name_plural = 'Official Leave Policy Numbers'

    ro = models.PositiveSmallIntegerField(default=9, verbose_name='Rollover')
    pl = models.PositiveSmallIntegerField(default=18, verbose_name='Max. Personal Leave/year')
    sl = models.PositiveSmallIntegerField(default=12, verbose_name='Max. Sick Leave/year')
    mt = models.PositiveSmallIntegerField(default=180, verbose_name='Maternity Leave')
    pt = models.PositiveSmallIntegerField(default=7, verbose_name='Paternity Leave')
    ma = models.PositiveSmallIntegerField(default=1, verbose_name='Marriage')

    eplm = models.FloatField(default=1.5, verbose_name='Earned Personal Leave/month')
    eslm = models.FloatField(default=1.0, verbose_name='Earned Sick Leave/month')
    mplcb = models.FloatField(default=3.0, verbose_name='Max. Personal Leave(Borrow/Consultant)')
    mpscb = models.FloatField(default=3.0, verbose_name='Max. Sick Leave(Borrow/Consultant)')
    mpleb = models.FloatField(default=5.0, verbose_name='Max. Personal Leave(Borrow/Employee)')
    mpseb = models.FloatField(default=5.0, verbose_name='Max. Sick Leave(Borrow/Employee)')

        
    def __str__(self):
        return "LeavesSchedule"


class Profile(models.Model):

    class Meta:
        verbose_name = 'Employee/Consultant Profile'
        verbose_name_plural = 'Employee/filterConsultant Profile'

    user = models.OneToOneField(
        User, to_field='username',
        on_delete=models.CASCADE)
    
    employee_name = models.CharField(max_length=75)

    role = models.BooleanField(default=True,verbose_name="Consultant")

    rollover = models.PositiveSmallIntegerField(default=0)

    region = models.ForeignKey(Region, on_delete=models.PROTECT)

    lm_start_date = models.DateField(verbose_name="Start Date(leave calculation)")

    approver = models.BooleanField(default=False)

    approver_id = models.ForeignKey(
        User, to_field='username', on_delete=models.CASCADE,
        related_name='my_approver',
        verbose_name='Approver',
    )
    
    GENDER = [('M', 'Male'), ('F', 'Female')]
    Gender = models.CharField(choices=GENDER, default='M', max_length=1)

    token=models.CharField(max_length=500,default=uuid4())

    def __str__(self):
        return self.employee_name


class records(models.Model):
    class Meta:
        verbose_name = 'Leave Records'
        verbose_name_plural = 'Leave Records'
    
    LEAVECHOICES = [
        ('PERFD', "Personal"),
        ('PERHD', "Personal (Half Day)"),
        ('SICFD', "Sick"),
        ('SICHD', "Sick (Half Day)"),
        ('MATER', "Maternity"),
        ('PATER', "Paternity"),
        ('MARRY', "Marriage"),
        ('LOPFD', "Loss of Pay"),
        ('LOPHD', "Loss of Pay (Half Day)"),
        ]
    
    PARTIAL_DAY_CHOICE = [
        ('FIRHALF', "First Half"),
        ('SECHALF', "Second Half"),
    ]
    
    user = models.ForeignKey(
        User, to_field='username',
        on_delete=models.CASCADE)

    recname = models.CharField(max_length=75, default='name')

    approved = models.BooleanField(default=False)
    
    from_date = models.DateField(verbose_name='Date')

    leave_period = models.CharField(
        choices=PARTIAL_DAY_CHOICE,
        default='FIRHALF', max_length=9)
    
    num_days = models.FloatField(default=0)
    
    reason = models.CharField(
        choices=LEAVECHOICES,
        default='PERFD', max_length=18)
    
    approver_id = models.ForeignKey(
        User, to_field='username',
        on_delete=models.CASCADE,
        related_name='approver',
        verbose_name='Approver')
    
    approved_date = models.DateField(
        auto_now=True,
        auto_now_add=False)
    
    add_date = models.DateField(auto_now=True)
    
    year = models.PositiveSmallIntegerField()

    cancelled = models.BooleanField(default=False)
    

    property
    def isin_future(self):
        return date.today() <= self.from_date

    def __str__(self):
        return f'{self.from_date} {self.reason}'
