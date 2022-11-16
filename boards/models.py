from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.utils.html import mark_safe
from markdown import markdown
import math


# Create your models here.


class Board(models.Model):
    name = models.CharField(max_length=30,
                            unique=True, )  # In the Board model definition, more specifically in the name field, we are also setting the parameter unique=True, as the name suggests, it will enforce the uniqueness of the field at the database level.
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()






class Topic(models.Model):
    subject = models.CharField(
        max_length=255)  # Some fields have required arguments, such as the CharField. We should always set a max_length. This information will be used to create the database column. Django needs to know how big the database column needs to be. The max_length parameter will also be used by the Django Forms API, to validate user input.
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(
        Board, related_name='topics', on_delete=models.CASCADE, )
    starter = models.ForeignKey(
        User, related_name='topics', on_delete=models.CASCADE, )
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject

    def get_page_count(self):
        count = self.posts.count()
        pages = count / 20
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)

    def get_last_ten_posts(self):
        return self.posts.order_by('-created_at')[:10]


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(
        Topic, related_name='posts',
        on_delete=models.CASCADE, )  # In the Post model, the created_at field has an optional parameter, the auto_now_add set to True. This will instruct Django to set the current date and time when a Post object is created.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(
        User, related_name='posts', on_delete=models.CASCADE, )
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE, )

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))