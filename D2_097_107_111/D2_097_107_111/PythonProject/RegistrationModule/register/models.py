from django.db import models

# Create your models here.
class Customer(models.Model):
    c_username=models.CharField(max_length=15,primary_key=True)
    c_name=models.CharField(max_length=30)
    c_address=models.CharField(max_length=50)
    c_mobileno=models.IntegerField()
    c_email=models.CharField(max_length=30)
    c_password=models.CharField(max_length=20)

class Admin(models.Model):
    AD_ID=models.CharField(max_length=15,primary_key=True)
    AD_password=models.CharField(max_length=15)

class Event(models.Model):
    event_ID=models.IntegerField(auto_created=True,primary_key=True)
    event_name=models.CharField(max_length=30)
    event_type=models.CharField(max_length=20)
    event_duration=models.IntegerField()
    event_time=models.TimeField()
    event_date=models.DateField()
    event_venue=models.CharField(max_length=15)
    event_description=models.TextField()
    event_image=models.ImageField(upload_to="event-images")
    event_contact_no=models.IntegerField()

class Images(models.Model):
    event_ID=models.ForeignKey(Event,on_delete=models.CASCADE)
    more_images=models.ImageField(upload_to="more-images")

class Videos(models.Model):
    event_ID=models.ForeignKey(Event,on_delete=models.CASCADE)
    more_videos=models.FileField(upload_to="more-videos")

class Manager(models.Model):
    m_username=models.CharField(max_length=15,primary_key=True)
    m_name=models.CharField(max_length=30)
    m_address=models.CharField(max_length=50)
    m_mobileno=models.IntegerField()
    m_email=models.CharField(max_length=30)
    m_event_type=models.CharField(max_length=15)
    m_password=models.CharField(max_length=20)

class ManagerEvent(models.Model):
    m_username=models.ForeignKey(Manager,on_delete=models.CASCADE)
    event_ID=models.ForeignKey(Event,on_delete=models.CASCADE)
    m_event_status=models.CharField(max_length=15)

class AdminEvent(models.Model):
    AD_ID=models.ForeignKey(Admin,on_delete=models.CASCADE)
    event_ID=models.ForeignKey(Event,on_delete=models.CASCADE)

class Feedback(models.Model):
    F_ID=models.CharField(max_length=20)
    feedback=models.TextField()
    date=models.DateTimeField(auto_now=True)

class CustomerEvent(models.Model):
    m_username=models.CharField(max_length=15)
    c_username=models.ForeignKey(Customer,on_delete=models.CASCADE)
    event_type=models.CharField(max_length=20)
    event_venue=models.CharField(max_length=15)
    event_cost=models.IntegerField()
    event_time=models.TimeField()
    event_date=models.DateField()
    event_status=models.CharField(max_length=15)