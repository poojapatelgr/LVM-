from django.urls import path
from . import views
from .views import index


app_name = 'tokenauth'


urlpatterns = [
        path('accounts/register/',views.registration,name="registration"),
        path('token/<slug:token>',views.tokenloginurl,name="tokenloginv1"),
]
