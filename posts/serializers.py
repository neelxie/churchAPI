from rest_framework import serializers
from .models import Post, POST_TYPE, NOTE_TYPE


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'approved', 'mediaUrl',
                  'post_type', 'passage', ) 