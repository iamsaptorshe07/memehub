from django.db import models
from accounts.models import UserProfile
from django.db.models.signals import post_delete
from django.dispatch import receiver 
from django.utils import timezone

# Create your models here.

def photos_upload(instance, filename):
    return  f"users/{instance.author.email}/photos/{filename}"

def videos_upload(instance, filename):
    return f"users/{instance.author.email }/videos/{filename}"
   
class Meme(models.Model):
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='author')
    photos = models.ImageField(verbose_name='Upload Photo',upload_to=photos_upload,)
    videos = models.FileField(verbose_name='Upload Video',upload_to=videos_upload, )
    caption  = models.CharField(verbose_name='Enter Caption',max_length=500,blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    meme_text = models.TextField(verbose_name='Enter Meme')
    likes = models.ManyToManyField(UserProfile, default=None, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(UserProfile, default=None, blank=True, related_name='dislikes')

    def __str__(self):
        return 'created at ' + str(self.created_date) + ' by ' + self.author.email

@receiver(post_delete, sender=Meme)
def submission_delete(sender, instance, **kwargs):
    instance.photos.delete(False)
    instance.videos.delete(False)

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    content_updated = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True)

    def __str__(self):
        if self.parent is None:
            return 'Comment by '+ self.user.email + ' on meme-id ' + str(self.meme.id)
        else:
            return  'Reply by '+ self.user.email + ' on comment-id ' + str(self.parent.id) + ' of meme-id ' + str(self.meme.id) 
