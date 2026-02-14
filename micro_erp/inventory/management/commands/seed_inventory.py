from micro_erp.inventory.models import StockMovement, StockLevel, Product, Location
from django.core.management.base import BaseCommand
from faker import Faker

class Command(BaseCommand):
    help = "Seed the inventory database with mock data."

    def handle(self, *args, **options):
        fake = Faker()

        # Clean the database to avoid duplicates
        self.stdout.write("Cleaning inventory tables...")
        StockMovement.objects.all().delete()
        StockLevel.objects.all().delete()
        Product.objects.all().delete()
        Location.objects.all().delete()

        # Create locations
        self.stdout.write("Seeding locations...")
        Location.objects.create(name='Warehouse', address=fake.address())
        Location.objects.create(name="Location A", address=fake.address())
        Location.objects.create(name="Location B", address=fake.address())

        # Create products
        self.stdout.write("Seeding products...")
        Product.objects.create(name='Product A')
        Product.objects.create(name='Product B')
        Product.objects.create(name='Product C')

        # Create stock levels
        self.stdout.write("Seeding stock levels...")
        for product in Product.objects.all():
            for location in Location.objects.all():
                StockLevel.objects.create(product=product, location=location, quantity=fake.random_int(min=0, max=100))

        self.stdout.write("Seeding stock movements...")

        # Create mock data for stock movements
        for _ in range(10):
            product = Product.objects.order_by('?').first()
            quantity = fake.random_int(min=1, max=10)
            movement_type = fake.random_element(['IN', 'OUT', 'TR'])
            from_location = Location.objects.order_by('?').first() if movement_type in ['OUT', 'TR'] else None
            to_location = Location.objects.order_by('?').first() if movement_type in ['IN', 'TR'] else None
            unit_price_at_purchase = fake.random_int(min=1, max=100) if movement_type == 'IN' else None
            reference = fake.sentence()

            StockMovement.objects.create(
                product=product,
                quantity=quantity,
                movement_type=movement_type,
                from_location=from_location,
                to_location=to_location,
                unit_price_at_purchase=unit_price_at_purchase,
                reference=reference
            )
        
        self.stdout.write(self.style.SUCCESS("Successfully seeded inventory"))  