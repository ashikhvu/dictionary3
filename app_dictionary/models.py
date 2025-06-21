from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class dictionary_model(models.Model):
    eng_word = models.CharField(max_length=128)
    mal_word = models.CharField(max_length=128)

# curryshp

class User(AbstractUser):
    delivery_address = models.TextField(blank=True,null=True,default='')
    profile_image = models.ImageField(blank=True,null=True,upload_to='profile/images/')
    phone = models.CharField(max_length=15,blank=True,null=True,unique=False)

    def __str__(self):
        return self.username
    
class ProfileModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    order_filter_choices = (
        ('date','date'),
        ('type','type')
    )
    order_filter = models.CharField(max_length=255,default='type',choices=order_filter_choices)
    order_sort_choices = (
        ('accending','accending'),
        ('deccending','deccending')
    )
    order_sort = models.CharField(max_length=255,default='accending',choices=order_sort_choices)

    def __str__(self):
        return str(f'profile [ {self.user.username} ]')

class ItemModel(models.Model):
    name = models.CharField(max_length=255)
    des = models.TextField(blank=True,null=True)
    qty = models.IntegerField(default=0)
    prize = models.FloatField(default=0.00)
    cat_choices = (
        ('curry','curry'),
        ('shakes','shakes'),
        ('food','food'),
        ('ice cream','ice cream'),
        ('drinks','drinks')
    )
    category = models.CharField(max_length=255,choices=cat_choices,default='food')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/',blank=True,null=True)

    def __str__(self):
        return str(self.name)

class BillModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    billno = models.CharField(max_length=50,blank=True,null=True,unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
    grand_total = models.FloatField(default=0.00)
    paid = models.FloatField(default=0.00)
    bal = models.FloatField(default=0.00)
    order_status_status_choices = (
        ('ordered','ordered'),
        ('cancelled','cancelled'),
        ('delivered','delivered'),
    )
    order_status = models.CharField(max_length=50,default='ordered',choices=order_status_status_choices)
    ordered_time = models.DateTimeField(blank=True,null=True)
    accept_status_choices = (
        ('accepted','accepted'),
        ('notaccepted','notaccepted'),
        ('rejected','rejected')
    )
    accept_status = models.CharField(max_length=255,default='notaccepted',choices=accept_status_choices)
    reject_reason = models.TextField(blank=True,null=True)
    rejected_user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name='rejected_user_details')
    accept_or_reject_time = models.DateTimeField(blank=True,null=True)
    prepared_status_choices = (
        ('prepared','prepared'),
        ('notprepared','notprepared')
    )
    prepared_status = models.CharField(max_length=255,default='notprepared',choices=prepared_status_choices)
    prepared_time = models.DateTimeField(blank=True,null=True)
    packed_status_choices = (
        ('packed','packed'),
        ('notpacked','notpacked')
    )
    packed_status = models.CharField(max_length=255,default='notpacked',choices=packed_status_choices)
    packed_time = models.DateTimeField(blank=True,null=True)
    ready_status_choices = (
        ('ready','ready'),
        ('notready','notready'),
    )
    ready_status = models.CharField(max_length=50,default='notready',choices=ready_status_choices)
    ready_time = models.DateTimeField(blank=True,null=True)
    called_status_choices = (
        ('called','called'),
        ('notcalled','notcalled'),
    )
    called_status = models.CharField(max_length=50,default='notcalled',choices=called_status_choices) 
    called_time = models.DateTimeField(blank=True,null=True)
    dispatched_status_choices = (
        ('dispatched','dispatched'),
        ('notdispatched','notdispatched')
    )
    dispatched_status = models.CharField(max_length=255,default='notdispatched',choices=dispatched_status_choices)
    dispatched_time = models.DateTimeField(blank=True,null=True)
    delivered_status_choices = (
        ('delevered','delevered'),
        ('notdelevered','notdelevered'),
    )
    delevered_status = models.CharField(max_length=255,default='notdelevered',choices=delivered_status_choices)
    delevered_time = models.DateTimeField(blank=True,null=True)

    expected_delevery_time = models.DateTimeField(blank=True,null=True)
    

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)        
        self.billno = f"Bill-{self.id}"
        super().save(*args,**kwargs)        

    def __str__(self):
        return str(self.id)
    

class ItemlistModel(models.Model):
    bill = models.ForeignKey(BillModel,on_delete=models.CASCADE,related_name="itemlistmodel",blank=True,null=True)
    name = models.CharField(max_length=255)
    prize = models.FloatField(default=0.00)
    qty = models.IntegerField(default=0,blank=True,null=True)
    total = models.IntegerField(default=0)

    def __str__(self):
        return self.name