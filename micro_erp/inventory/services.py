from django.db import transaction
from micro_erp.inventory.models import StockMovement, StockLevel

@transaction.atomic
def create_stock_movement(product, quantity, movement_type, from_location=None, to_location=None, unit_price_at_purchase=None, reference=None):
    movement = StockMovement.objects.create(
        product=product,
        quantity=quantity,
        movement_type=movement_type,
        from_location=from_location,
        to_location=to_location,
        unit_price_at_purchase=unit_price_at_purchase,
        reference=reference,
    )

    if movement_type in ['OUT', 'TR'] and from_location:
        stock = StockLevel.objects.get(product=product, location=from_location)
        stock.quantity -= quantity
        stock.save()
        
    if movement_type in ['IN', 'TR'] and to_location:
        stock, _ = StockLevel.objects.get_or_create(
            product=product,
            location=to_location, 
            defaults={'quantity': 0}
        )
        stock.quantity += quantity
        stock.save()
        
    return movement