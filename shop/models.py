from django.db import models

# Create your models here.
class Categorydetail(models.Model):
    category_name = models.CharField(max_length=100)
    category_image = models.ImageField(upload_to='shop/category', default="")
    
    
    def __str__(self):
        return self.category_name


class product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=200)
    category_name = models.ForeignKey(Categorydetail, on_delete=models.CASCADE, blank=True, null=True)
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=1000)
    pub_date = models.DateField()
    image = models.ImageField(upload_to='shop/images', default="")


    def __str__(self):
        return self.product_name

class contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=1000, default="")
    

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    item_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=120)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=90)
    state = models.CharField(max_length=90)
    zip_code = models.CharField(max_length=90)
    phone = models.CharField(max_length=90, default="")


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.update_desc[0:7] + "..."