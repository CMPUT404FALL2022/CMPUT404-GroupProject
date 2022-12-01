from django.db import models
        
class Node(models.Model):
    host = models.CharField(primary_key=True, max_length=255, null=False)
    api = models.CharField(max_length=255, null=False)
    authorization = models.CharField(max_length=255, null=False)