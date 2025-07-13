from django.db import models

class logininfo(models.Model):
    username = models.CharField(max_length=200)
    password =  models.CharField(max_length=200)


# check if UserName and Password matches
# Then sign in, else deny entry


#manually make usersnames and passwords -> 
#reroute employee accounts to home.url
#reroute admin accounts to adminurl