from django.urls import path
from micro_erp.inventory.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]