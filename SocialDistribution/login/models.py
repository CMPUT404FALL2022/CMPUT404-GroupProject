from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class users(models.Model):
    username = models.CharField(unique=True,max_length=12,blank=False, null=False, validators=[MinLengthValidator(3)])
    password = models.CharField(max_length=18,blank=False, null=False, validators=[MinLengthValidator(6)])
    uid = models.CharField(unique=True,max_length=200)
    user_type = models.CharField(max_length=200)

    # create a unique id for each new user
    # def generate_unique_id(self):
    #     unique_id = uuid.uuid4()
    
    def __str__(self):
        return {"username":self.username,"pass":self.password,"uid":self.uid,"user_type":self.user_type}
        



