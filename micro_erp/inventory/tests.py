from django.test import TestCase
from micro_erp.inventory.services import create_stock_movement, InsufficientStockError
from micro_erp.inventory.models import Location, Product, StockLevel, StockMovement

# Create your tests here.

class InventoryTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.warehouse = Location.objects.create(name='Warehouse', address='123 Main St')
        cls.location_a = Location.objects.create(name='Location 1', address='456 Elm St')
        cls.location_b = Location.objects.create(name='Location 2', address='789 Oak St')

        cls.product_a = Product.objects.create(name='Product A')
        cls.product_b = Product.objects.create(name='Product B')
        cls.product_c = Product.objects.create(name='Product C')
        
        cls.stock_a = StockLevel.objects.create(product=cls.product_a, location=cls.warehouse, quantity=10)
        cls.stock_b = StockLevel.objects.create(product=cls.product_a, location=cls.location_a, quantity=5)
        cls.stock_c = StockLevel.objects.create(product=cls.product_b, location=cls.warehouse, quantity=20)
        cls.stock_d = StockLevel.objects.create(product=cls.product_b, location=cls.location_b, quantity=15)

    def test_total_inventory(self):
        self.assertEqual(self.product_a.total_inventory, 15)
        self.assertEqual(self.product_b.total_inventory, 35)

    def test_stock_movements(self):
        create_stock_movement(
            product=self.product_a,
            quantity=5,
            movement_type='TR',
            from_location=self.warehouse,
            to_location=self.location_a
        )

        self.stock_a.refresh_from_db()
        self.stock_b.refresh_from_db()

        self.assertEqual(self.stock_a.quantity, 5)
        self.assertEqual(self.stock_b.quantity, 10)

        create_stock_movement(
            product=self.product_b,
            quantity=10,
            movement_type='IN',
            to_location=self.warehouse
        )

        self.stock_c.refresh_from_db()
        self.stock_d.refresh_from_db()

        self.assertEqual(self.stock_c.quantity, 30)

        create_stock_movement(
            product=self.product_a,
            quantity=5,
            movement_type='OUT',
            from_location=self.location_a
        )

        self.stock_b.refresh_from_db()

        self.assertEqual(self.stock_b.quantity, 5)
    
    def test_insufficient_stock(self):
        with self.assertRaises(InsufficientStockError):
            create_stock_movement(
                product=self.product_a,
                quantity=15,
                movement_type='OUT',
                from_location=self.location_a
            )
        
        self.assertEqual(StockMovement.objects.count(), 0)