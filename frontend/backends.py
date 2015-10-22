from django.contrib.auth.backends import ModelBackend
from frontend.models import CustomUser
 
class CaseInsensitiveModelBackend(ModelBackend):
  """
  By default ModelBackend does case _sensitive_ username authentication, which isn't what is
  generally expected.  This backend supports case insensitive username authentication.
  """
  def authenticate(self, username=None, password=None):
    try:
      user = CustomUser.objects.get(email__iexact=username)
      if user.check_password(password):
        return user
      else:
        return None
    except CustomUser.DoesNotExist:
      return None
