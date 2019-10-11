from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

# choices for the post type
TEXT = 'T'
VIDEO = 'V'
AUDIO = 'A'

# choices for the notification type
APPROVED = 'P'
REJECTED = 'R'
NEW_POST = 'N'

# tuple for post type
POST_TYPE = (
  (TEXT, 'Text'),
  (VIDEO, 'Video'),
  (AUDIO, 'Audio')
)
NOTE_TYPE = (
    (APPROVED, 'Approved'),
    (REJECTED, 'Rejected'),
    (NEW_POST, 'New_post')
)

class Church(models.Model):
    name = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
 
class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):

        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.email_verified = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # Each `User` needs a human-readable unique identifier that we can use to
    # represent the `User` in the UI. We want to index this column in the
    # database to improve lookup performance.
    username = models.CharField(db_index=True, max_length=255, unique=True)

    # We also need a way to contact the user and a way for the user to identify
    # themselves when logging in. Since we need an email address for contacting
    # the user anyways, we will also use the email for logging in because it is
    # the most common form of login credential at the time of writing.
    email = models.EmailField(db_index=True, unique=True)
    name = models.CharField( max_length=255)
    google_id = models.CharField( max_length=255)

    # The `is_staff` flag is expected by Django to determine who can and cannot
    # log into the Django admin site. For most users, this flag will always be
    # falsed.
    is_staff = models.BooleanField(default=True)

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)
    # More fields required by Django when specifying a custom user model.

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case, we want that to be the email field.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()



class Upload(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(
        User,
        related_name='uploader_name',
        on_delete=models.CASCADE)
    uploadUrl = models.URLField(max_length=200)

class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)
    mediaUrl = models.URLField(max_length=200)
    post_type = models.CharField(max_length=1, choices=POST_TYPE,default=TEXT)
    passage = models.TextField()
    author = models.ForeignKey(
        User,
        related_name='post_author',
        on_delete=models.CASCADE)
    parentPost = models.ForeignKey('self', blank=True, related_name='subposts')
    updated_at = models.DateTimeField(auto_now_add=True)
    #relatedUpload = models.ForeignKey(Upload, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Notification(models.Model):
    note_text = models.CharField(max_length=100)
    note_type = models.CharField(max_length=1, choices=NOTE_TYPE,default=NEW_POST)
    seen = models.BooleanField(default=False)
    recipient = models.ForeignKey(
        User,
        related_name='note_recipient',
        on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    relatedPost = models.ForeignKey(Post, on_delete=models.CASCADE)