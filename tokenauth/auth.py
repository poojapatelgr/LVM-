from django.contrib.auth.backends import BaseBackend
from .models import Profile

class MyBackend(BaseBackend):
    def authenticate(self, request, token=None):
        if request.method == 'POST':
            token=request.POST['token']
            user=Profile.objects.get(token=token)
            print(user)
