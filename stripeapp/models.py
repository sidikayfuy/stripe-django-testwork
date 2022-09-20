from django.db import models
import stripe


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    price = models.IntegerField(default=0)
    currency = models.CharField(max_length=3, default='rub')

    def __str__(self):
        return self.name


class Discount(models.Model):
    code = models.CharField(max_length=100)
    discount = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        stripe.Coupon.create(duration="once", id=self.id, percent_off=self.discount)

    def __str__(self):
        return self.code


class Promocode(models.Model):
    code = models.CharField(max_length=100)
    coupon = models.ForeignKey(Discount, on_delete=models.CASCADE, default=None)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        stripe.PromotionCode.create(coupon=self.coupon.id, code=self.code)

    def __str__(self):
        return self.code

class Tax(models.Model):
    name = models.CharField(max_length=100)
    inclusive = models.BooleanField(default=False)
    percentage = models.FloatField()
    country = models.CharField(max_length=3)
    desc = models.CharField(max_length=100)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        stripe.TaxRate.create(display_name=self.name, inclusive=self.inclusive, percentage=self.percentage, country=self.country, description=self.desc)

    def __str__(self):
        return self.desc

