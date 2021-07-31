from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

"""
===============================================================
*We need 3- fields here:
------------------------
* BODY :For the text post.
* TIME: The date and time details of the creation of the post.
* AUTHOR: The user who created the post.
================================================================
"""

# For Posts:


class Post(models.Model):
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(
        User, blank=True, related_name='dislikes')

# For comments:


class Comment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    likes = models.ManyToManyField(
        User, blank=True, related_name='comment_likes')
    # For child comment:
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')

    # Adding Property methods: It will allow us to access a function within the actual template itself:

    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-created_on').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

# For Profiles:


class UserProfile(models.Model):
    # Using 'OneToOneField'==> One profile for one user and One user per Profile i.e. 'one for each'.
    user = models.OneToOneField(User, primary_key=True, verbose_name='user',
                                related_name='profile', on_delete=models.CASCADE)
    # 'blank' & 'null' are TRUE here because at the time of initiation of the profile, nothing should be pre-filled.
    name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to='uploads/profile_pictures',
                                default='uploads/profile_pictures/default_user.png', blank=True)
    cover = models.ImageField(upload_to='uploads/cover_pictures',
                              default='uploads/cover_pictures/default_cover.png', blank=True)
    # For followers:
    followers = models.ManyToManyField(
        User, blank=True, related_name='followers')
    userNotifications = models.ManyToManyField(
        User, blank=True, related_name='notifications')

    # For automatic profile creation we need:

    """
    sender - User
    receiver - decorator(@receiver)
    instance - User object being saved
    created - true/false
    """


@receiver(post_save, sender=User)  # receiver is decorator.
def create_user_profile(sender, instance, created, **kwargs):
    """
    We're just creating the user, not saving it in the database.
    And setting the User to be instance which in this case is the user sender which is created.
    """

    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Now this is for saving the User Profile in the database.
    Here Sender is the user model, instance is user object that is saved.
    """
    instance.profile.save()


# Notification:

class Notification(models.Model):
    # 1 ==> Like, 2 ==> Comment, 3 ==> Follow
    notification_type = models.IntegerField()
    """
    There will be two user foreign keys:
    1st: 'to-user'- to whom: the notification is being sent to.
    2nd: 'from-user'- from whom: the notification has been sent from.
    """
    to_user = models.ForeignKey(
        User, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(
        User, related_name='notification_from', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    comment = models.ForeignKey(
        'Comment', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)
