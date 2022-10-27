from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class single_author(AbstractBaseUser):
    type = "author"
    username = models.CharField(primary_key=True,unique=True,max_length=255,default='')
    password = models.CharField(validators=[MinLengthValidator(6)],max_length=255,default='')
    id = models.CharField(unique=True,max_length=255,blank=True,null=True)
    host = models.CharField(max_length=255,default='',blank=True)
    display_name = models.CharField(max_length=255,blank=True,default='')
    url = models.URLField(blank=True,default='')
    github = models.URLField(blank=True,default='')
    profileImage = models.ImageField(upload_to='avatars/', blank=True,null=True)

    USERNAME_FIELD = 'username'

    # create a unique id for each new user
    # def generate_unique_id(self):
    #     unique_id = uuid.uuid4()
    
    def __str__(self):
        return 'type:'+self.type+ 'id:'+ self.id+'host:'+ self.host+'display_name'+ self.display_name+'url'+ self.url+'github'+ self.github

class followRequest(models.Model):
    type = "Follow"
    summary = models.TextField(max_length=25, blank=True,default='')
    actor = models.ForeignKey(to=single_author,on_delete=models.CASCADE,related_name='request_sender')
    object = models.ForeignKey(to=single_author,on_delete=models.CASCADE,related_name='request_receiver')

class Followers(models.Model):
    type = 'Followers'
    user = models.OneToOneField(to=single_author,on_delete=models.CASCADE,related_name='user')
    items = models.ManyToManyField(to=single_author, related_name='items', blank=True)