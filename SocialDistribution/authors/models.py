from email.policy import default
from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class single_author(models.Model):
    type = "author"
    username = models.CharField(primary_key=True,unique=True,max_length=255)
    password = models.CharField(validators=[MinLengthValidator(6)],max_length=255)
    id = models.CharField(unique=True,max_length=255,blank=True)
    host = models.CharField(max_length=255,default='',blank=True)
    display_name = models.CharField(max_length=255,blank=True)
    url = models.URLField(blank=True)
    github = models.URLField(blank=True)
    profileImage = models.ImageField(blank=True)

    # create a unique id for each new user
    # def generate_unique_id(self):
    #     unique_id = uuid.uuid4()
    
    def __str__(self):
        return 'type:'+self.type+ 'id:'+ self.id+'host:'+ self.host+'display_name'+ self.display_name+'url'+ self.url+'github'+ self.github

def authors(models.Model):
    type = "authors"
    items = models.ManyToManyField(single_author)