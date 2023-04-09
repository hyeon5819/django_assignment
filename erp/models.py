from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# 상품 모델
class Product(models.Model):
    code = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=256)
    inbound_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0) # 출고 가격=판매 가격
    sizes = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('F', 'Free'),
    )
    size = models.CharField(choices=sizes, max_length=1)
    stock_quantity = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.code}: {self.name}'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.stock_quantity = 0
            super().save(*args, **kwargs)
            
            # inventory 생성
            Inventory.objects.create(product=self, inbound_quantity=0, outbound_quantity=0)
        else:
            super().save(*args, **kwargs)

    # inventory 값 저장시 product의 stock_quantity 최신화 메서드
    def update_stock_quantity(self): 
        inventory = self.inventory
        inbound_quantity = inventory.inbound_quantity
        outbound_quantity = inventory.outbound_quantity
        inventory_stock_quantity = inbound_quantity + outbound_quantity
        self.stock_quantity = inventory_stock_quantity


# 입고 모델
class Inbound(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


# 출고 모델
class Outbound(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


# inventory 모델
class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True, related_name='inventory')
    product_name = models.CharField(max_length=50, blank=True)
    inbound_quantity = models.IntegerField(default=0)
    outbound_quantity = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.product.name} Inventory'

    def save(self, *args, **kwargs):
        self.product_name = self.product.name
        super().save(*args, **kwargs)

        # inventory inbound/outbound 값 변경시 product의 stock_quantity 최신화
        self.product.update_stock_quantity()
        self.product.save()