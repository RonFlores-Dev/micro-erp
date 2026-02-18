from django.urls import path
from micro_erp.inventory.views import HomeView, StockMovementListView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('stock_movements/', StockMovementListView.as_view(), name='stock_movements'),
]