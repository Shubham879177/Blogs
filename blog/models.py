from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Post(models.Model):
     sno= models.AutoField(primary_key=True,)
     title= models.CharField(max_length=255, default="")
     author= models.CharField(max_length=100, default="")
     content= models.TextField()
     slug=models.CharField(max_length=20, default="")
     timeStamp=models.DateTimeField(blank=True, default="")

    
    
     def __str__(self):
        return f"{(self.title)} by {self.author}"
    