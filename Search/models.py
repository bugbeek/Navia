from django.db import models


class Medicine(models.Model):
    """
    Model for medicine data
    """
    sku_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    sku_name = models.CharField(max_length=300, null= True, blank=True)
    price = models.FloatField(blank=True,null=True)
    manufacturer_name = models.CharField(max_length=100, blank=True, null=True)
    salt_name = models.CharField(max_length=300, blank=True, null=True)
    drug_form = models.CharField(max_length=300, blank=True, null=True)
    Pack_size = models.CharField(max_length=300, blank=True, null=True)
    strength = models.CharField(max_length=300, blank=True, null=True)
    product_banned_flag = models.BooleanField(default=False, blank=True, null=True)
    unit = models.CharField(max_length=100, blank=True, null=True)
    price_per_unit = models.FloatField(blank=True, null=True)

    
    def __str__(self):
        return self.sku_name