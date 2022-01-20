from django.contrib import admin
from leaveman.models import Profile
from leaveman.models import records
from leaveman.models import Holidays
from leaveman.models import Region
from leaveman.models import LeavesPerYear

admin.site.register(Profile)
admin.site.register(records)
admin.site.register(Holidays)
admin.site.register(Region)
admin.site.register(LeavesPerYear)

