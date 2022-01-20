from django.urls import path
from .import views
from .forms import LeaveForm, TokenForm
from .views import applyleave
from .views import index
from .views import approved_history
from .views import isapprover,holidays, olt
from django.contrib.auth import views as auth_views



app_name = 'leaveman'

urlpatterns = [
    path("logout/", views.logout_request, name= "logout"),
    path('start/', isapprover, name="start"),
    path('new/', applyleave, name="new"),
    path('index/', index, name='index'),
    path('approved_history/', approved_history, name='approved_history'),
    path('delete_leave/<int:pk>',views.DeleteLeave,name='delete_leave'),
    path('filter/',views.exportCSV,name='filter'),
    path('export/',views.export_filter,name='export'),
    path('holidays/',views.holidays,name='holidays'),
    path('emp_history/<str:username>',views.employee_history,name='emp_history'),
    path('ls_history/',views.EmpHistory,name='ls_history'),
    path('help/',views.help,name='help'),
    path('olt/',views.olt,name='olt')
]

