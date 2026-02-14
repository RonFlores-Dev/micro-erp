from io import StringIO
from django.core.management import call_command
from django.test import TestCase
from micro_erp.inventory.models import StockMovement, StockLevel, Product, Location

class SeederTest(TestCase):

    def test_seeder(self):
        out = StringIO()

        call_command('seed_inventory', stdout=out)

        self.assertIn("Seeding locations...", out.getvalue())
        self.assertIn("Seeding products...", out.getvalue())
        self.assertIn("Seeding stock levels...", out.getvalue())
        self.assertIn("Seeding stock movements...", out.getvalue())

        self.assertEqual(Location.objects.count(), 3)
        self.assertEqual(Product.objects.count(), 3)
        self.assertEqual(StockLevel.objects.count(), 9)
        self.assertEqual(StockMovement.objects.count(), 10)