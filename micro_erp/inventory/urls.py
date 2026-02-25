from django.urls import path
from micro_erp.inventory.views import HomeView, StockMovementListView, StockLevelJsonView

urlpatterns = [
    path('<int:location_id>/', HomeView.as_view(), name='home'),
    path('stock_movements/<int:location_id>', StockMovementListView.as_view(), name='stock_movements'),
    path('stock_levels/<int:location_id>/', StockLevelJsonView.as_view(), name='stock_level'),
]