from django.db import models

# Create your models here.
class users(models.Model):
    username = models.CharField(min_length=3,max_length=12,blank=False, null=False)
    password = models.CharField(min_length=6,max_length=18,blank=False, null=False)
    uid = models.CharField()
    type = models.CharField()

    # create a unique id for each new user
    # def generate_unique_id(self):
    #     unique_id = uuid.uuid4()



