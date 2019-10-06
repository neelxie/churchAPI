from django.db import models

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


class Upload(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    #uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    uploadUrl = models.URLField(max_length=200)

class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)
    mediaUrl = models.URLField(max_length=200)
    post_type = models.CharField(max_length=1, choices=POST_TYPE,default=TEXT)
    passage = models.TextField()
    #author = models.ForeignKey(User, on_delete=models.CASCADE)
    parentPost = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now_add=True)
    #relatedUpload = models.ForeignKey(Upload, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Notification(models.Model):
    note_text = models.CharField(max_length=100)
    note_type = models.CharField(max_length=1, choices=NOTE_TYPE,default=NEW_POST)
    seen = models.BooleanField(default=False)
    #recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    relatedPost = models.ForeignKey(Post, on_delete=models.CASCADE)