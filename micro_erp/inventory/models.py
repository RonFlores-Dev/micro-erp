from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError

# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    locations = models.ManyToManyField(Location, through="StockLevel")

    @property
    def total_inventory(self):
        return self.stocklevel_set.aggregate(total=Sum('quantity'))['total'] or 0

    def __str__(self):
        return self.name
    
class StockLevel(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('product', 'location')
    
class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('IN', 'Inbound (Supplier)'),
        ('OUT', 'Outbound (Sale/Waste)'),
        ('TR', 'Internal Transfer'),
    ]

    STATUS = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('CANCELLED', 'Cancelled'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES)

    from_location = models.ForeignKey(
        Location, on_delete=models.PROTECT, 
        related_name='outbound_movement',
        null=True, blank=True
    )
    to_location = models.ForeignKey(
        Location, on_delete=models.PROTECT,
        related_name='inbound_movement',
        null=True, blank=True
    )

    unit_price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    # * Verified by manager, will be added in the future
    status = models.CharField(max_length=10, choices=STATUS, default='PENDING')
    
    timestamp = models.DateTimeField(auto_now_add=True)
    reference = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Stock Movement'
        indexes = [
            models.Index(fields=['product', 'timestamp'])
        ]

    def clean(self):
        if self.movement_type == 'TR' and not (self.from_location and self.to_location):
            raise ValidationError("Internal transfers require both a source and destination.")
        
        if self.movement_type == 'IN' and not self.to_location:
            raise ValidationError("Inbound movements require a destination location.")
            
        if self.movement_type == 'OUT' and not self.from_location:
            raise ValidationError("Outbound movements require a source location.")

    @property
    def total_cost(self):
        if self.unit_price_at_purchase and self.quantity:
            return self.unit_price_at_purchase * self.quantity
        return 0

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"