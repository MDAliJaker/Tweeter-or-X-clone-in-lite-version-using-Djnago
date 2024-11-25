from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class tweets(models.Model):
    user = models.ForeignKey(User, related_name="tweets", on_delete=models.DO_NOTHING )
    body= models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return( 
            f"{self.user}  "
            f"({ self.created_at :%Y-%m-%d %H:%M}): "
            f"{self.body}..."
        
        )


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name= 'followed_by', symmetrical=False, blank=True)
    date_modified = models.DateTimeField(user, auto_now=True)
    def __str__(self):
        return self.user.username
    
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([user_profile.id])
        user_profile.save()


post_save.connect(create_profile, sender=User)