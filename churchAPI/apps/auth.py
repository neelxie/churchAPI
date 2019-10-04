# using the secrets libraries are for generating random 
# strings for times when a site has users with same name
import secrets
import string
from django.core.exceptions import ValidationError
from .models import User


class ValidateUser:
    """
    This class checks
    whether a user exists in the system or not
    """
    # create a random str to append to a username
    # incase users from a site have the same name
    random_chars = ''.join(
                        secrets.choice(
                            string.ascii_letters) for i in range(7))
    def validate_user(self, this_user):
        try:
            current_user = User.objects.get(email=this_user.get("email"))
            return {
                "email": current_user.email,
                "token": current_user.token
            }
        except User.DoesNotExist:

            new_user = {
                'email': this_user.get('email'),
                'username': this_user.get(
                    'name' + self.random_chars,
                    "churchuserunkown" + self.random_chars),
                'password': User.objects.make_random_password()}

            app_user = User.objects.create_user(**new_user)
            app_user.is_active = True
            app_user.save()

            return {
                'email': this_user.get('email'),
                'token': app_user.token
            }
