from .models import Superuser
from rest_framework import authentication
from rest_framework import exceptions

class ExampleAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        if request.headers.get('X-USERNAME') == None:
            return None
        username = request.headers['X-USERNAME'] # get the username request header
            
        if not username: # no username passed in request headers
            return None # authentication did not succeed

        try:
            user = Superuser.objects.get(name=username) # get the user
        except Superuser.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user') # raise exception if user does not exist 

        return (user, None) # authentication successful