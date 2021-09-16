from django.db import models


# Create your models here.
class eCell(models.Model):
    id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=50, default='null')
    legal_name = models.CharField(max_length=50, default='null')
    college = models.CharField(max_length=100, default="IIIT-D")
    join_date = models.DateField(auto_now_add=True)
